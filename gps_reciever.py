#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# Author: 19ana
# GNU Radio version: 3.10.7.0

from packaging.version import Version as StrictVersion
from PyQt5 import Qt
from gnuradio import qtgui
import os
import sys
sys.path.append(os.environ.get('GRC_HIER_PATH', os.path.expanduser('~/.grc_gnuradio')))

from Xcorr import Xcorr  # grc-generated hier_block
from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio.qtgui import Range, RangeWidget
from PyQt5 import QtCore
import sip



class GPS_RECEIVER_ACCUISITION(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except BaseException as exc:
            print(f"Qt GUI: Could not set Icon: {str(exc)}", file=sys.stderr)
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "GPS_RECEIVER_ACCUISITION")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except BaseException as exc:
            print(f"Qt GUI: Could not restore geometry: {str(exc)}", file=sys.stderr)

        ##################################################
        # Variables
        ##################################################
        self.vector_size = vector_size = 2*1023
        self.samp_rate = samp_rate = 2*1023*1000
        self.doppler_freq = doppler_freq = 0
        self.code_delay = code_delay = 2
        self.Ncycle = Ncycle = 1

        ##################################################
        # Blocks
        ##################################################

        self._doppler_freq_range = Range(-7000, 7000, 100, 0, 200)
        self._doppler_freq_win = RangeWidget(self._doppler_freq_range, self.set_doppler_freq, "'doppler_freq'", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._doppler_freq_win)
        self._code_delay_range = Range(2, 2*1024, 1, 2, 200)
        self._code_delay_win = RangeWidget(self._code_delay_range, self.set_code_delay, "code delay", "counter_slider", float, QtCore.Qt.Horizontal)
        self.top_layout.addWidget(self._code_delay_win)
        self.qtgui_time_sink_x_1 = qtgui.time_sink_f(
            (vector_size*Ncycle), #size
            1, #samp_rate
            "", #name
            1, #number of inputs
            None # parent
        )
        self.qtgui_time_sink_x_1.set_update_time(0.10)
        self.qtgui_time_sink_x_1.set_y_axis(-20, 300)

        self.qtgui_time_sink_x_1.set_y_label('Amplitude', "")

        self.qtgui_time_sink_x_1.enable_tags(True)
        self.qtgui_time_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0.0, 0, 0, "")
        self.qtgui_time_sink_x_1.enable_autoscale(False)
        self.qtgui_time_sink_x_1.enable_grid(False)
        self.qtgui_time_sink_x_1.enable_axis_labels(True)
        self.qtgui_time_sink_x_1.enable_control_panel(True)
        self.qtgui_time_sink_x_1.enable_stem_plot(False)


        labels = ['Corr mag', 'Signal 2', 'Signal 3', 'Signal 4', 'Signal 5',
            'Signal 6', 'Signal 7', 'Signal 8', 'Signal 9', 'Signal 10']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ['blue', 'red', 'green', 'black', 'cyan',
            'magenta', 'yellow', 'dark red', 'dark green', 'dark blue']
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]
        styles = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
            -1, -1, -1, -1, -1]


        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_1.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_1.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_time_sink_x_1_win = sip.wrapinstance(self.qtgui_time_sink_x_1.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_1_win)
        self.digital_scrambler_bb_0_0 = digital.scrambler_bb(0x197, 0x3ff, 9)
        self.digital_scrambler_bb_0_0.set_block_alias("G2 scrambler")
        self.digital_scrambler_bb_0 = digital.scrambler_bb(0x81, 0x3ff, 9)
        self.digital_scrambler_bb_0.set_block_alias("G1 scrambler")
        self.digital_map_bb_0 = digital.map_bb([-1,1])
        self.digital_map_bb_0.set_block_alias("SV12CA MAP TO SV12GC")
        self.blocks_xor_xx_0_0_2_3_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_2_3 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_2_2_1 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_2_2_0_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_2_2_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_2_2 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_2_1_1_1 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_2_1_1_0_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_2_1_1_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_2_1_1 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_2_1_0_0_1 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_2_1_0_0_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_2_1_0_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_2_1 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_2_0_2_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_2_0_2 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_2_0_1_1 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_2_0_1_0_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_2_0_1_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_2_0_1 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_2_0_0_1_1 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_2_0_0_1_0_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_2_0_0_1_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_2_0_0_1 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_2_0_0_0_0_1 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_2_0_0_0_0_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_2_0_0_0_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_2_0_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_2_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_2 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_1_0_3_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_1_0_3 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_1_0_2_1 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_1_0_2_0_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_1_0_2_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_1_0_2 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_1_0_1_1_1 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_1_0_1_1_0_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_1_0_1_1_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_1_0_1_1 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_1_0_1_0_0_1 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_1_0_1_0_0_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_1_0_1_0_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_1_0_1 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_1_0_0_2_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_1_0_0_2 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_1_0_0_1_1 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_1_0_0_1_0_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_1_0_0_1_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_1_0_0_1 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_1_0_0_0_1_1 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_1_0_0_0_1_0_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_1_0_0_0_1_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_1_0_0_0_1 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_1_0_0_0_0_0_1 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_1_0_0_0_0_0_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_1_0_0_0_0_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_1_0_0_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_1_0_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_1_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_1 = blocks.xor_bb()
        self.blocks_xor_xx_0_0_0 = blocks.xor_bb()
        self.blocks_xor_xx_0_0 = blocks.xor_bb()
        self.blocks_xor_xx_0 = blocks.xor_bb()
        self.blocks_wavfile_source_0 = blocks.wavfile_source('C:\\Users\\19ana\\OneDrive\\Desktop\\Fall 2023\\ECE 492\\gps reciever rev 1\\sv12ca-1600recording1-7-2024', True)
        self.blocks_throttle2_0 = blocks.throttle( gr.sizeof_char*1, 1023000, True, 0 if "auto" == "auto" else max( int(float(0.1) * 1023000) if "auto" == "time" else int(0.1), 1) )
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_char*1, 2)
        self.blocks_repeat_0.set_block_alias("SV12CA intrpltn")
        self.blocks_null_sink_0_4 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_3_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_3 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_2_1 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_2_0_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_2_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_2 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_1_2 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_1_1_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_1_1 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_1_0_1 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_1_0_0_1_0_1 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_1_0_0_1_0_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_1_0_0_1_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_1_0_0_1 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_1_0_0_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_1_0_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_1_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_1 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_0_3 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_0_2_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_0_2 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_0_1_1 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_0_1_0_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_0_1_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_0_1 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_0_0_2 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_0_0_1_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_0_0_1 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_0_0_0_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_0_0_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_0_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_null_sink_0 = blocks.null_sink(gr.sizeof_char*1)
        self.blocks_multiply_xx_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_0.set_block_alias("RF IN * DOPPER FREQUENCY SV12CA")
        self.blocks_float_to_complex_1 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0.set_block_alias("SV12CA FLOAT TO CMPLX")
        self.blocks_delay_0_2_0 = blocks.delay(gr.sizeof_char*1, 1)
        self.blocks_delay_0_2_0.set_block_alias("G1 D1")
        self.blocks_delay_0_2 = blocks.delay(gr.sizeof_char*1, 1)
        self.blocks_delay_0_2.set_block_alias("G2 D1")
        self.blocks_delay_0_1_2_0 = blocks.delay(gr.sizeof_char*1, 1)
        self.blocks_delay_0_1_2_0.set_block_alias("G1 D3")
        self.blocks_delay_0_1_2 = blocks.delay(gr.sizeof_char*1, 1)
        self.blocks_delay_0_1_2.set_block_alias("G2 D3")
        self.blocks_delay_0_1_1_0_0 = blocks.delay(gr.sizeof_char*1, 1)
        self.blocks_delay_0_1_1_0_0.set_block_alias("G1 D7")
        self.blocks_delay_0_1_1_0 = blocks.delay(gr.sizeof_char*1, 1)
        self.blocks_delay_0_1_1_0.set_block_alias("G2 D7")
        self.blocks_delay_0_1_0_1_0 = blocks.delay(gr.sizeof_char*1, 1)
        self.blocks_delay_0_1_0_1_0.set_block_alias("G1 D5")
        self.blocks_delay_0_1_0_1 = blocks.delay(gr.sizeof_char*1, 1)
        self.blocks_delay_0_1_0_1.set_block_alias("G2 D5")
        self.blocks_delay_0_1_0_0_0_1 = blocks.delay(gr.sizeof_char*1, 1)
        self.blocks_delay_0_1_0_0_0_1.set_block_alias("G1 D9")
        self.blocks_delay_0_1_0_0_0_0_0 = blocks.delay(gr.sizeof_char*1, 1)
        self.blocks_delay_0_1_0_0_0_0_0.set_block_alias("G1 D10")
        self.blocks_delay_0_1_0_0_0_0 = blocks.delay(gr.sizeof_char*1, 1)
        self.blocks_delay_0_1_0_0_0_0.set_block_alias("G2 D10")
        self.blocks_delay_0_1_0_0_0 = blocks.delay(gr.sizeof_char*1, 1)
        self.blocks_delay_0_1_0_0_0.set_block_alias("G2 D9")
        self.blocks_delay_0_0_2_0 = blocks.delay(gr.sizeof_char*1, 1)
        self.blocks_delay_0_0_2_0.set_block_alias("G1 D2")
        self.blocks_delay_0_0_2 = blocks.delay(gr.sizeof_char*1, 1)
        self.blocks_delay_0_0_2.set_block_alias("G2 D2")
        self.blocks_delay_0_0_1_0_0 = blocks.delay(gr.sizeof_char*1, 1)
        self.blocks_delay_0_0_1_0_0.set_block_alias("G1 D6")
        self.blocks_delay_0_0_1_0 = blocks.delay(gr.sizeof_char*1, 1)
        self.blocks_delay_0_0_1_0.set_block_alias("G2 D6")
        self.blocks_delay_0_0_0_1_0 = blocks.delay(gr.sizeof_char*1, 1)
        self.blocks_delay_0_0_0_1_0.set_block_alias("G1 D4")
        self.blocks_delay_0_0_0_1 = blocks.delay(gr.sizeof_char*1, 1)
        self.blocks_delay_0_0_0_1.set_block_alias("G2 D4")
        self.blocks_delay_0_0_0_0_0_0 = blocks.delay(gr.sizeof_char*1, 1)
        self.blocks_delay_0_0_0_0_0_0.set_block_alias("G1 D8")
        self.blocks_delay_0_0_0_0_0 = blocks.delay(gr.sizeof_char*1, 1)
        self.blocks_delay_0_0_0_0_0.set_block_alias("G2 D8")
        self.blocks_delay_0 = blocks.delay(gr.sizeof_gr_complex*1, code_delay)
        self.blocks_delay_0.set_block_alias("SV12CA DELAY 2")
        self.blocks_complex_to_mag_squared_0 = blocks.complex_to_mag_squared(1)
        self.blocks_char_to_float_1 = blocks.char_to_float(1, 1)
        self.blocks_char_to_float_1.set_block_alias("SV12CA BIT TO FLOAT")
        self.analog_sig_source_x_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, doppler_freq, 1, 0, 0)
        self.analog_sig_source_x_0_0.set_block_alias("DOPPLER FOR SV12CA")
        self.analog_const_source_x_1 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 0)
        self.analog_const_source_x_0 = analog.sig_source_b(0, analog.GR_CONST_WAVE, 0, 0, 0)
        self.Xcorr_0 = Xcorr(
            Ncycle=1,
            samp_rate=(2*1023000),
            vector_size=(2*1023),
        )
        self.Xcorr_0.set_block_alias("XCORR PRMT AND DPLR RF")


        ##################################################
        # Connections
        ##################################################
        self.connect((self.Xcorr_0, 0), (self.blocks_complex_to_mag_squared_0, 0))
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_throttle2_0, 0))
        self.connect((self.analog_const_source_x_1, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.analog_sig_source_x_0_0, 0), (self.blocks_multiply_xx_0, 1))
        self.connect((self.blocks_char_to_float_1, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_complex_to_mag_squared_0, 0), (self.qtgui_time_sink_x_1, 0))
        self.connect((self.blocks_delay_0, 0), (self.Xcorr_0, 0))
        self.connect((self.blocks_delay_0_0_0_0_0, 0), (self.blocks_delay_0_1_0_0_0, 0))
        self.connect((self.blocks_delay_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_2, 1))
        self.connect((self.blocks_delay_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_2_0_0_0_0, 1))
        self.connect((self.blocks_delay_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_2_0_0_1_1, 0))
        self.connect((self.blocks_delay_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_2_0_1_0_0, 1))
        self.connect((self.blocks_delay_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_2_1_1_0, 0))
        self.connect((self.blocks_delay_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_2_1_1_0_0, 1))
        self.connect((self.blocks_delay_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_2_2_1, 1))
        self.connect((self.blocks_delay_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_2_3, 1))
        self.connect((self.blocks_delay_0_0_0_0_0_0, 0), (self.blocks_delay_0_1_0_0_0_1, 0))
        self.connect((self.blocks_delay_0_0_0_1, 0), (self.blocks_delay_0_1_0_1, 0))
        self.connect((self.blocks_delay_0_0_0_1, 0), (self.blocks_xor_xx_0_0_2, 0))
        self.connect((self.blocks_delay_0_0_0_1, 0), (self.blocks_xor_xx_0_0_2_0_0, 0))
        self.connect((self.blocks_delay_0_0_0_1, 0), (self.blocks_xor_xx_0_0_2_0_0_1_0_0, 0))
        self.connect((self.blocks_delay_0_0_0_1, 0), (self.blocks_xor_xx_0_0_2_0_2_0, 0))
        self.connect((self.blocks_delay_0_0_0_1, 0), (self.blocks_xor_xx_0_0_2_1_0_0_0, 1))
        self.connect((self.blocks_delay_0_0_0_1, 0), (self.blocks_xor_xx_0_0_2_1_1, 1))
        self.connect((self.blocks_delay_0_0_0_1_0, 0), (self.blocks_delay_0_1_0_1_0, 0))
        self.connect((self.blocks_delay_0_0_1_0, 0), (self.blocks_delay_0_1_1_0, 0))
        self.connect((self.blocks_delay_0_0_1_0, 0), (self.blocks_xor_xx_0, 1))
        self.connect((self.blocks_delay_0_0_1_0, 0), (self.blocks_xor_xx_0_0_2_0_0_1, 1))
        self.connect((self.blocks_delay_0_0_1_0, 0), (self.blocks_xor_xx_0_0_2_0_1_0_0, 0))
        self.connect((self.blocks_delay_0_0_1_0, 0), (self.blocks_xor_xx_0_0_2_0_1_1, 0))
        self.connect((self.blocks_delay_0_0_1_0, 0), (self.blocks_xor_xx_0_0_2_0_2_0, 1))
        self.connect((self.blocks_delay_0_0_1_0, 0), (self.blocks_xor_xx_0_0_2_1, 1))
        self.connect((self.blocks_delay_0_0_1_0, 0), (self.blocks_xor_xx_0_0_2_1_0_0, 0))
        self.connect((self.blocks_delay_0_0_1_0, 0), (self.blocks_xor_xx_0_0_2_1_0_0_1, 1))
        self.connect((self.blocks_delay_0_0_1_0_0, 0), (self.blocks_delay_0_1_1_0_0, 0))
        self.connect((self.blocks_delay_0_0_2, 0), (self.blocks_delay_0_1_2, 0))
        self.connect((self.blocks_delay_0_0_2, 0), (self.blocks_xor_xx_0, 0))
        self.connect((self.blocks_delay_0_0_2, 0), (self.blocks_xor_xx_0_0_2_0_0_0_0_0, 0))
        self.connect((self.blocks_delay_0_0_2, 0), (self.blocks_xor_xx_0_0_2_0_0_0_0_1, 0))
        self.connect((self.blocks_delay_0_0_2, 0), (self.blocks_xor_xx_0_0_2_0_1, 0))
        self.connect((self.blocks_delay_0_0_2, 0), (self.blocks_xor_xx_0_0_2_0_1_0, 0))
        self.connect((self.blocks_delay_0_0_2, 0), (self.blocks_xor_xx_0_0_2_0_2, 0))
        self.connect((self.blocks_delay_0_0_2_0, 0), (self.blocks_delay_0_1_2_0, 0))
        self.connect((self.blocks_delay_0_1_0_0_0, 0), (self.blocks_delay_0_1_0_0_0_0, 0))
        self.connect((self.blocks_delay_0_1_0_0_0, 0), (self.blocks_xor_xx_0_0_2_0, 1))
        self.connect((self.blocks_delay_0_1_0_0_0, 0), (self.blocks_xor_xx_0_0_2_0_0_1_0, 0))
        self.connect((self.blocks_delay_0_1_0_0_0, 0), (self.blocks_xor_xx_0_0_2_0_0_1_0_0, 1))
        self.connect((self.blocks_delay_0_1_0_0_0, 0), (self.blocks_xor_xx_0_0_2_0_1_1, 1))
        self.connect((self.blocks_delay_0_1_0_0_0, 0), (self.blocks_xor_xx_0_0_2_0_2, 1))
        self.connect((self.blocks_delay_0_1_0_0_0, 0), (self.blocks_xor_xx_0_0_2_1_1_0, 1))
        self.connect((self.blocks_delay_0_1_0_0_0, 0), (self.blocks_xor_xx_0_0_2_1_1_1, 1))
        self.connect((self.blocks_delay_0_1_0_0_0, 0), (self.blocks_xor_xx_0_0_2_2, 1))
        self.connect((self.blocks_delay_0_1_0_0_0_0, 0), (self.blocks_null_sink_0_1_0_0_1_0, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_0, 0), (self.blocks_xor_xx_0_0_2_0_0_1_0, 1))
        self.connect((self.blocks_delay_0_1_0_0_0_0, 0), (self.blocks_xor_xx_0_0_2_0_0_1_1, 1))
        self.connect((self.blocks_delay_0_1_0_0_0_0, 0), (self.blocks_xor_xx_0_0_2_0_1, 1))
        self.connect((self.blocks_delay_0_1_0_0_0_0, 0), (self.blocks_xor_xx_0_0_2_2_0, 1))
        self.connect((self.blocks_delay_0_1_0_0_0_0_0, 0), (self.blocks_null_sink_0_1_0_0_1, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_0, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_1, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_1_0, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_1_0_0, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_1_0_0_0, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_1_0_0_0_0_0, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_1_0_0_0_0_0_0, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_1_0_0_0_0_0_1, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_1_0_0_0_1, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_1_0_0_0_1_0, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_1_0_0_0_1_0_0, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_1_0_0_0_1_1, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_1_0_0_1, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_1_0_0_1_0, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_1_0_0_1_0_0, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_1_0_0_1_1, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_1_0_0_2, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_1_0_0_2_0, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_1_0_1, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_1_0_1_0_0, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_1_0_1_0_0_0, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_1_0_1_0_0_1, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_1_0_1_1, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_1_0_1_1_0, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_1_0_1_1_0_0, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_1_0_1_1_1, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_1_0_2, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_1_0_2_0, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_1_0_2_0_0, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_1_0_2_1, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_1_0_3, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_1_0_3_0, 0))
        self.connect((self.blocks_delay_0_1_0_0_0_1, 0), (self.blocks_delay_0_1_0_0_0_0_0, 0))
        self.connect((self.blocks_delay_0_1_0_1, 0), (self.blocks_delay_0_0_1_0, 0))
        self.connect((self.blocks_delay_0_1_0_1, 0), (self.blocks_xor_xx_0_0_2_0, 0))
        self.connect((self.blocks_delay_0_1_0_1, 0), (self.blocks_xor_xx_0_0_2_0_0_0_0_0, 1))
        self.connect((self.blocks_delay_0_1_0_1, 0), (self.blocks_xor_xx_0_0_2_0_0_1, 0))
        self.connect((self.blocks_delay_0_1_0_1, 0), (self.blocks_xor_xx_0_0_2_2_0_0, 0))
        self.connect((self.blocks_delay_0_1_0_1, 0), (self.blocks_xor_xx_0_0_2_2_1, 0))
        self.connect((self.blocks_delay_0_1_0_1_0, 0), (self.blocks_delay_0_0_1_0_0, 0))
        self.connect((self.blocks_delay_0_1_1_0, 0), (self.blocks_delay_0_0_0_0_0, 0))
        self.connect((self.blocks_delay_0_1_1_0, 0), (self.blocks_xor_xx_0_0, 1))
        self.connect((self.blocks_delay_0_1_1_0, 0), (self.blocks_xor_xx_0_0_2_0_0, 1))
        self.connect((self.blocks_delay_0_1_1_0, 0), (self.blocks_xor_xx_0_0_2_0_0_0_0, 0))
        self.connect((self.blocks_delay_0_1_1_0, 0), (self.blocks_xor_xx_0_0_2_0_0_0_0_1, 1))
        self.connect((self.blocks_delay_0_1_1_0, 0), (self.blocks_xor_xx_0_0_2_1_0_0, 1))
        self.connect((self.blocks_delay_0_1_1_0, 0), (self.blocks_xor_xx_0_0_2_1_1_1, 0))
        self.connect((self.blocks_delay_0_1_1_0, 0), (self.blocks_xor_xx_0_0_2_2_0_0, 1))
        self.connect((self.blocks_delay_0_1_1_0_0, 0), (self.blocks_delay_0_0_0_0_0_0, 0))
        self.connect((self.blocks_delay_0_1_2, 0), (self.blocks_delay_0_0_0_1, 0))
        self.connect((self.blocks_delay_0_1_2, 0), (self.blocks_xor_xx_0_0, 0))
        self.connect((self.blocks_delay_0_1_2, 0), (self.blocks_xor_xx_0_0_2_0_1_0, 1))
        self.connect((self.blocks_delay_0_1_2, 0), (self.blocks_xor_xx_0_0_2_1, 0))
        self.connect((self.blocks_delay_0_1_2, 0), (self.blocks_xor_xx_0_0_2_1_1, 0))
        self.connect((self.blocks_delay_0_1_2, 0), (self.blocks_xor_xx_0_0_2_1_1_0_0, 0))
        self.connect((self.blocks_delay_0_1_2, 0), (self.blocks_xor_xx_0_0_2_2_0, 0))
        self.connect((self.blocks_delay_0_1_2, 0), (self.blocks_xor_xx_0_0_2_3_0, 1))
        self.connect((self.blocks_delay_0_1_2_0, 0), (self.blocks_delay_0_0_0_1_0, 0))
        self.connect((self.blocks_delay_0_2, 0), (self.blocks_delay_0_0_2, 0))
        self.connect((self.blocks_delay_0_2, 0), (self.blocks_xor_xx_0_0_2_1_0_0_0, 0))
        self.connect((self.blocks_delay_0_2, 0), (self.blocks_xor_xx_0_0_2_1_0_0_1, 0))
        self.connect((self.blocks_delay_0_2, 0), (self.blocks_xor_xx_0_0_2_2, 0))
        self.connect((self.blocks_delay_0_2, 0), (self.blocks_xor_xx_0_0_2_3, 0))
        self.connect((self.blocks_delay_0_2, 0), (self.blocks_xor_xx_0_0_2_3_0, 0))
        self.connect((self.blocks_delay_0_2_0, 0), (self.blocks_delay_0_0_2_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_float_to_complex_1, 0), (self.blocks_multiply_xx_0, 0))
        self.connect((self.blocks_multiply_xx_0, 0), (self.Xcorr_0, 1))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_char_to_float_1, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.digital_scrambler_bb_0, 0))
        self.connect((self.blocks_throttle2_0, 0), (self.digital_scrambler_bb_0_0, 0))
        self.connect((self.blocks_wavfile_source_0, 0), (self.blocks_float_to_complex_1, 0))
        self.connect((self.blocks_wavfile_source_0, 1), (self.blocks_float_to_complex_1, 1))
        self.connect((self.blocks_xor_xx_0, 0), (self.blocks_xor_xx_0_0_0, 1))
        self.connect((self.blocks_xor_xx_0_0, 0), (self.blocks_xor_xx_0_0_1, 1))
        self.connect((self.blocks_xor_xx_0_0_0, 0), (self.blocks_null_sink_0_1_0_0_1_0_0, 0))
        self.connect((self.blocks_xor_xx_0_0_1, 0), (self.blocks_null_sink_0_1_0_0_1_0_1, 0))
        self.connect((self.blocks_xor_xx_0_0_1_0, 0), (self.blocks_null_sink_0_1_0_0, 0))
        self.connect((self.blocks_xor_xx_0_0_1_0_0, 0), (self.blocks_null_sink_0_0_1_0, 0))
        self.connect((self.blocks_xor_xx_0_0_1_0_0_0, 0), (self.blocks_null_sink_0_2_0_0, 0))
        self.connect((self.blocks_xor_xx_0_0_1_0_0_0_0_0, 0), (self.blocks_null_sink_0_0_0, 0))
        self.connect((self.blocks_xor_xx_0_0_1_0_0_0_0_0_0, 0), (self.blocks_null_sink_0_1_0_0_0, 0))
        self.connect((self.blocks_xor_xx_0_0_1_0_0_0_0_0_1, 0), (self.blocks_null_sink_0_1_2, 0))
        self.connect((self.blocks_xor_xx_0_0_1_0_0_0_1, 0), (self.blocks_null_sink_0_0_1, 0))
        self.connect((self.blocks_xor_xx_0_0_1_0_0_0_1, 0), (self.digital_map_bb_0, 0))
        self.connect((self.blocks_xor_xx_0_0_1_0_0_0_1_0, 0), (self.blocks_null_sink_0_0, 0))
        self.connect((self.blocks_xor_xx_0_0_1_0_0_0_1_0_0, 0), (self.blocks_null_sink_0_4, 0))
        self.connect((self.blocks_xor_xx_0_0_1_0_0_0_1_1, 0), (self.blocks_null_sink_0_2_1, 0))
        self.connect((self.blocks_xor_xx_0_0_1_0_0_1, 0), (self.blocks_null_sink_0_0_0_1, 0))
        self.connect((self.blocks_xor_xx_0_0_1_0_0_1_0, 0), (self.blocks_null_sink_0_0_0_0, 0))
        self.connect((self.blocks_xor_xx_0_0_1_0_0_1_0_0, 0), (self.blocks_null_sink_0_1_0_1, 0))
        self.connect((self.blocks_xor_xx_0_0_1_0_0_1_1, 0), (self.blocks_null_sink_0_1_1_0, 0))
        self.connect((self.blocks_xor_xx_0_0_1_0_0_2, 0), (self.blocks_null_sink_0_0_2, 0))
        self.connect((self.blocks_xor_xx_0_0_1_0_0_2_0, 0), (self.blocks_null_sink_0_3_0, 0))
        self.connect((self.blocks_xor_xx_0_0_1_0_1, 0), (self.blocks_null_sink_0_0_1_0_0, 0))
        self.connect((self.blocks_xor_xx_0_0_1_0_1_0_0, 0), (self.blocks_null_sink_0_2, 0))
        self.connect((self.blocks_xor_xx_0_0_1_0_1_0_0_0, 0), (self.blocks_null_sink_0, 0))
        self.connect((self.blocks_xor_xx_0_0_1_0_1_0_0_1, 0), (self.blocks_null_sink_0_0_0_2, 0))
        self.connect((self.blocks_xor_xx_0_0_1_0_1_1, 0), (self.blocks_null_sink_0_1_0, 0))
        self.connect((self.blocks_xor_xx_0_0_1_0_1_1_0, 0), (self.blocks_null_sink_0_1, 0))
        self.connect((self.blocks_xor_xx_0_0_1_0_1_1_0_0, 0), (self.blocks_null_sink_0_0_3, 0))
        self.connect((self.blocks_xor_xx_0_0_1_0_1_1_1, 0), (self.blocks_null_sink_0_0_1_1, 0))
        self.connect((self.blocks_xor_xx_0_0_1_0_2, 0), (self.blocks_null_sink_0_2_0, 0))
        self.connect((self.blocks_xor_xx_0_0_1_0_2_0, 0), (self.blocks_null_sink_0_3, 0))
        self.connect((self.blocks_xor_xx_0_0_1_0_2_0_0, 0), (self.blocks_null_sink_0_0_0_0_0, 0))
        self.connect((self.blocks_xor_xx_0_0_1_0_2_1, 0), (self.blocks_null_sink_0_0_0_1_0, 0))
        self.connect((self.blocks_xor_xx_0_0_1_0_3, 0), (self.blocks_null_sink_0_1_1, 0))
        self.connect((self.blocks_xor_xx_0_0_1_0_3_0, 0), (self.blocks_null_sink_0_0_2_0, 0))
        self.connect((self.blocks_xor_xx_0_0_2, 0), (self.blocks_xor_xx_0_0_1_0, 1))
        self.connect((self.blocks_xor_xx_0_0_2_0, 0), (self.blocks_xor_xx_0_0_1_0_0, 1))
        self.connect((self.blocks_xor_xx_0_0_2_0_0, 0), (self.blocks_xor_xx_0_0_1_0_0_0, 1))
        self.connect((self.blocks_xor_xx_0_0_2_0_0_0_0, 0), (self.blocks_xor_xx_0_0_1_0_0_0_0_0, 1))
        self.connect((self.blocks_xor_xx_0_0_2_0_0_0_0_0, 0), (self.blocks_xor_xx_0_0_1_0_0_0_0_0_0, 1))
        self.connect((self.blocks_xor_xx_0_0_2_0_0_0_0_1, 0), (self.blocks_xor_xx_0_0_1_0_0_0_0_0_1, 1))
        self.connect((self.blocks_xor_xx_0_0_2_0_0_1, 0), (self.blocks_xor_xx_0_0_1_0_0_0_1, 1))
        self.connect((self.blocks_xor_xx_0_0_2_0_0_1_0, 0), (self.blocks_xor_xx_0_0_1_0_0_0_1_0, 1))
        self.connect((self.blocks_xor_xx_0_0_2_0_0_1_0_0, 0), (self.blocks_xor_xx_0_0_1_0_0_0_1_0_0, 1))
        self.connect((self.blocks_xor_xx_0_0_2_0_0_1_1, 0), (self.blocks_xor_xx_0_0_1_0_0_0_1_1, 1))
        self.connect((self.blocks_xor_xx_0_0_2_0_1, 0), (self.blocks_xor_xx_0_0_1_0_0_1, 1))
        self.connect((self.blocks_xor_xx_0_0_2_0_1_0, 0), (self.blocks_xor_xx_0_0_1_0_0_1_0, 1))
        self.connect((self.blocks_xor_xx_0_0_2_0_1_0_0, 0), (self.blocks_xor_xx_0_0_1_0_0_1_0_0, 1))
        self.connect((self.blocks_xor_xx_0_0_2_0_1_1, 0), (self.blocks_xor_xx_0_0_1_0_0_1_1, 1))
        self.connect((self.blocks_xor_xx_0_0_2_0_2, 0), (self.blocks_xor_xx_0_0_1_0_0_2, 1))
        self.connect((self.blocks_xor_xx_0_0_2_0_2_0, 0), (self.blocks_xor_xx_0_0_1_0_0_2_0, 1))
        self.connect((self.blocks_xor_xx_0_0_2_1, 0), (self.blocks_xor_xx_0_0_1_0_1, 1))
        self.connect((self.blocks_xor_xx_0_0_2_1_0_0, 0), (self.blocks_xor_xx_0_0_1_0_1_0_0, 1))
        self.connect((self.blocks_xor_xx_0_0_2_1_0_0_0, 0), (self.blocks_xor_xx_0_0_1_0_1_0_0_0, 1))
        self.connect((self.blocks_xor_xx_0_0_2_1_0_0_1, 0), (self.blocks_xor_xx_0_0_1_0_1_0_0_1, 1))
        self.connect((self.blocks_xor_xx_0_0_2_1_1, 0), (self.blocks_xor_xx_0_0_1_0_1_1, 1))
        self.connect((self.blocks_xor_xx_0_0_2_1_1_0, 0), (self.blocks_xor_xx_0_0_1_0_1_1_0, 1))
        self.connect((self.blocks_xor_xx_0_0_2_1_1_0_0, 0), (self.blocks_xor_xx_0_0_1_0_1_1_0_0, 1))
        self.connect((self.blocks_xor_xx_0_0_2_1_1_1, 0), (self.blocks_xor_xx_0_0_1_0_1_1_1, 1))
        self.connect((self.blocks_xor_xx_0_0_2_2, 0), (self.blocks_xor_xx_0_0_1_0_2, 1))
        self.connect((self.blocks_xor_xx_0_0_2_2_0, 0), (self.blocks_xor_xx_0_0_1_0_2_0, 1))
        self.connect((self.blocks_xor_xx_0_0_2_2_0_0, 0), (self.blocks_xor_xx_0_0_1_0_2_0_0, 1))
        self.connect((self.blocks_xor_xx_0_0_2_2_1, 0), (self.blocks_xor_xx_0_0_1_0_2_1, 1))
        self.connect((self.blocks_xor_xx_0_0_2_3, 0), (self.blocks_xor_xx_0_0_1_0_3, 1))
        self.connect((self.blocks_xor_xx_0_0_2_3_0, 0), (self.blocks_xor_xx_0_0_1_0_3_0, 1))
        self.connect((self.digital_map_bb_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.digital_scrambler_bb_0, 0), (self.blocks_delay_0_2_0, 0))
        self.connect((self.digital_scrambler_bb_0_0, 0), (self.blocks_delay_0_2, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "GPS_RECEIVER_ACCUISITION")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_vector_size(self):
        return self.vector_size

    def set_vector_size(self, vector_size):
        self.vector_size = vector_size

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.analog_sig_source_x_0_0.set_sampling_freq(self.samp_rate)

    def get_doppler_freq(self):
        return self.doppler_freq

    def set_doppler_freq(self, doppler_freq):
        self.doppler_freq = doppler_freq
        self.analog_sig_source_x_0_0.set_frequency(self.doppler_freq)

    def get_code_delay(self):
        return self.code_delay

    def set_code_delay(self, code_delay):
        self.code_delay = code_delay
        self.blocks_delay_0.set_dly(int(self.code_delay))

    def get_Ncycle(self):
        return self.Ncycle

    def set_Ncycle(self, Ncycle):
        self.Ncycle = Ncycle




def main(top_block_cls=GPS_RECEIVER_ACCUISITION, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
