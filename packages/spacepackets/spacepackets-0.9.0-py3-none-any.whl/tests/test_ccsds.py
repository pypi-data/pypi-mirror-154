from unittest import TestCase
from collections import deque

from spacepackets.ccsds.spacepacket import (
    get_space_packet_sequence_control,
    SpacePacketHeader,
    PacketTypes,
    get_space_packet_id_bytes,
    get_space_packet_id_num,
    SequenceFlags,
    get_apid_from_raw_space_packet,
    get_space_packet_header,
    parse_space_packets,
)
from spacepackets.ecss.tm import PusTelemetry, PusVersion


class TestCcsds(TestCase):
    def test_spacepacket(self):
        sp_header = SpacePacketHeader(
            apid=0x02,
            data_length=22,
            ssc=52,
            packet_type=PacketTypes.TC,
            sequence_flags=SequenceFlags.FIRST_SEGMENT,
        )
        self.assertEqual(sp_header.apid, 0x02)
        self.assertEqual(sp_header.ssc, 52)
        self.assertEqual(sp_header.data_length, 22)
        self.assertEqual(sp_header.packet_type, PacketTypes.TC)
        sp_packed = sp_header.pack()
        self.assertEqual(get_apid_from_raw_space_packet(raw_packet=sp_packed), 0x02)
        self.assertRaises(
            ValueError, get_apid_from_raw_space_packet, raw_packet=bytearray()
        )
        sp_unpacked = SpacePacketHeader.unpack(space_packet_raw=sp_packed)
        self.assertRaises(
            ValueError,
            SpacePacketHeader,
            apid=982292,
            data_length=22,
            ssc=52,
            packet_type=PacketTypes.TC,
        )
        self.assertRaises(
            ValueError,
            SpacePacketHeader,
            apid=0x02,
            data_length=679393,
            ssc=52,
            packet_type=PacketTypes.TC,
        )
        self.assertRaises(
            ValueError,
            SpacePacketHeader,
            apid=0x02,
            data_length=22,
            ssc=96030,
            packet_type=PacketTypes.TC,
        )
        self.assertRaises(ValueError, SpacePacketHeader.unpack, bytearray())
        self.assertEqual(sp_unpacked.packet_type, PacketTypes.TC)
        self.assertEqual(sp_unpacked.apid, 0x02)
        self.assertEqual(sp_unpacked.version, 0b000)
        self.assertEqual(sp_unpacked.ssc, 52)
        self.assertEqual(sp_unpacked.sequence_flags, SequenceFlags.FIRST_SEGMENT)
        print(sp_header)
        print(sp_header.__repr__())

        byte_one, byte_two = get_space_packet_id_bytes(
            packet_type=PacketTypes.TC, apid=0x3FF, secondary_header_flag=True
        )
        self.assertEqual(byte_two, 0xFF)
        self.assertEqual(byte_one & 0x07, 0x03)
        packet_id_as_num = byte_one << 8 | byte_two
        packet_id = get_space_packet_id_num(
            packet_type=PacketTypes.TC, apid=0x3FF, secondary_header_flag=True
        )
        self.assertEqual(packet_id_as_num, packet_id)

        psc = get_space_packet_sequence_control(
            source_sequence_count=0x22, sequence_flags=SequenceFlags.UNSEGMENTED
        )
        sequence_flags_raw = psc >> 14
        ssc_raw = psc & 0x3FFF
        self.assertEqual(sequence_flags_raw, SequenceFlags.UNSEGMENTED)
        self.assertEqual(ssc_raw, 0x22)
        self.assertRaises(
            ValueError,
            get_space_packet_sequence_control,
            source_sequence_count=0xFFFF,
            sequence_flags=SequenceFlags.UNSEGMENTED,
        )
        self.assertRaises(
            ValueError,
            get_space_packet_sequence_control,
            source_sequence_count=0x3FFF,
            sequence_flags=5,
        )

        raw_header = get_space_packet_header(
            packet_id=packet_id, packet_sequence_control=psc, data_length=22
        )
        self.assertEqual(raw_header[0], ((packet_id & 0xFF00) >> 8) & 0x1FFF)
        self.assertEqual(raw_header[1], packet_id & 0xFF)
        self.assertEqual(raw_header[2], (psc & 0xFF00) >> 8)
        self.assertEqual(raw_header[3], psc & 0xFF)
        self.assertEqual(raw_header[4], (22 & 0xFF00) >> 8)
        self.assertEqual(raw_header[5], 22 & 0xFF)

        header_from_composite = SpacePacketHeader.from_composite_fields(
            packet_id=packet_id, psc=psc, data_length=22
        )
        self.assertEqual(header_from_composite.pack(), raw_header)
        header_tm = SpacePacketHeader(
            packet_type=PacketTypes.TM,
            sequence_flags=SequenceFlags.UNSEGMENTED,
            apid=0x12,
            data_length=7,
            ssc=28,
        )
        raw = header_tm.pack()
        header_tm_back = SpacePacketHeader.unpack(raw)
        self.assertEqual(header_tm_back.packet_type, PacketTypes.TM)
        self.assertEqual(header_tm_back.apid, 0x12)
        self.assertEqual(header_tm_back.version, 0b000)
        self.assertEqual(header_tm_back.ssc, 28)
        self.assertEqual(header_tm_back.data_length, 7)

    def test_sp_parser(self):
        tm_packet = PusTelemetry(service=17, subservice=2, pus_version=PusVersion.PUS_C)
        packet_ids = (tm_packet.packet_id,)
        tm_packet_raw = tm_packet.pack()
        packet_deque = deque()
        packet_deque.appendleft(tm_packet_raw)
        packet_deque.appendleft(tm_packet_raw)
        sp_list = parse_space_packets(
            analysis_queue=packet_deque, packet_ids=packet_ids
        )
        self.assertEqual(len(sp_list), 2)
        self.assertEqual(sp_list[0], tm_packet_raw)
        self.assertEqual(sp_list[1], tm_packet_raw)

        other_larger_packet = PusTelemetry(
            service=8,
            subservice=128,
            pus_version=PusVersion.PUS_C,
            source_data=bytearray(64),
        )
        other_larger_packet_raw = other_larger_packet.pack()
        packet_deque.appendleft(tm_packet_raw)
        packet_deque.appendleft(bytearray(8))
        packet_deque.appendleft(other_larger_packet_raw)
        sp_list = parse_space_packets(
            analysis_queue=packet_deque, packet_ids=packet_ids
        )
        self.assertEqual(len(sp_list), 2)
        self.assertEqual(sp_list[0], tm_packet_raw)
        self.assertEqual(sp_list[1], other_larger_packet_raw)

        packet_deque.appendleft(bytearray(3))
        sp_list = parse_space_packets(
            analysis_queue=packet_deque, packet_ids=packet_ids
        )
        self.assertEqual(len(sp_list), 0)
        sp_list = parse_space_packets(
            analysis_queue=packet_deque, packet_ids=packet_ids
        )
        self.assertEqual(len(sp_list), 0)

        # slice TM packet in half
        tm_packet_first_half = tm_packet_raw[:10]
        tm_packet_second_half = tm_packet_raw[10:]
        packet_deque.appendleft(tm_packet_first_half)
        sp_list = parse_space_packets(
            analysis_queue=packet_deque, packet_ids=packet_ids
        )
        self.assertEqual(len(sp_list), 0)
        self.assertEqual(len(packet_deque), 1)
        packet_deque.appendleft(tm_packet_second_half)
        sp_list = parse_space_packets(
            analysis_queue=packet_deque, packet_ids=packet_ids
        )
        self.assertEqual(len(sp_list), 1)
        self.assertEqual(len(packet_deque), 0)
        self.assertEqual(sp_list[0], tm_packet_raw)
