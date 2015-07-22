# Copyright (c) 2012 The WebRTC project authors. All Rights Reserved.
#
# Use of this source code is governed by a BSD-style license
# that can be found in the LICENSE file in the root of the source
# tree. An additional intellectual property rights grant can be found
# in the file PATENTS.  All contributing project authors may
# be found in the AUTHORS file in the root of the source tree.

{
  'targets': [
    {
      'target_name': 'iSACFix',
      'type': 'static_library',
      'dependencies': [
        '<(webrtc_root)/common_audio/common_audio.gyp:common_audio',
        '<(webrtc_root)/system_wrappers/system_wrappers.gyp:system_wrappers',
      ],
      'include_dirs': [
        'fix/interface',
        '<(webrtc_root)'
      ],
      'direct_dependent_settings': {
        'include_dirs': [
          'fix/interface',
          '<(webrtc_root)',
        ],
      },
      'sources': [
        'audio_encoder_isac_t.h',
        'audio_encoder_isac_t_impl.h',
        'fix/interface/audio_encoder_isacfix.h',
        'fix/interface/isacfix.h',
        'fix/source/arith_routines.c',
        'fix/source/arith_routines_hist.c',
        'fix/source/arith_routines_logist.c',
        'fix/source/audio_encoder_isacfix.cc',
        'fix/source/bandwidth_estimator.c',
        'fix/source/decode.c',
        'fix/source/decode_bwe.c',
        'fix/source/decode_plc.c',
        'fix/source/encode.c',
        'fix/source/entropy_coding.c',
        'fix/source/fft.c',
        'fix/source/filterbank_tables.c',
        'fix/source/filterbanks.c',
        'fix/source/filters.c',
        'fix/source/initialize.c',
        'fix/source/isacfix.c',
        'fix/source/lattice.c',
        'fix/source/lattice_c.c',
        'fix/source/lpc_masking_model.c',
        'fix/source/lpc_tables.c',
        'fix/source/pitch_estimator.c',
        'fix/source/pitch_estimator_c.c',
        'fix/source/pitch_filter.c',
        'fix/source/pitch_filter_c.c',
        'fix/source/pitch_gain_tables.c',
        'fix/source/pitch_lag_tables.c',
        'fix/source/spectrum_ar_model_tables.c',
        'fix/source/transform.c',
        'fix/source/transform_tables.c',
        'fix/source/arith_routins.h',
        'fix/source/bandwidth_estimator.h',
        'fix/source/codec.h',
        'fix/source/entropy_coding.h',
        'fix/source/fft.h',
        'fix/source/filterbank_tables.h',
        'fix/source/lpc_masking_model.h',
        'fix/source/lpc_tables.h',
        'fix/source/pitch_estimator.h',
        'fix/source/pitch_gain_tables.h',
        'fix/source/pitch_lag_tables.h',
        'fix/source/settings.h',
        'fix/source/spectrum_ar_model_tables.h',
        'fix/source/structs.h',
      ],
      'conditions': [
        ['OS!="win"', {
          'defines': [
            'WEBRTC_LINUX',
          ],
        }],
        ['winrt_platform=="win_phone" or winrt_platform=="win10_arm"', {
          'rules': [
          {
            'rule_name': 'gas_preprocessor',
            'extension': 'S',
            'inputs': [
             ],
             'outputs': [
               '<(INTERMEDIATE_DIR)/<(RULE_INPUT_ROOT).obj',
             ],
             'action': [
               'perl ../build/gas-preprocessor/gas-preprocessor.pl -as-type armasm -force-thumb -- armasm -oldit -I../../ -c <(RULE_INPUT_PATH) -o <(INTERMEDIATE_DIR)/<(RULE_INPUT_ROOT).obj'
             ],
             'process_outputs_as_sources': 0,
             'message': 'Compiling <(RULE_INPUT_PATH)',
           }],
         }],
        ['(target_arch=="arm" and arm_version>=7) or winrt_platform=="win_phone" or winrt_platform=="win10_arm"', {
          'sources': [
            'fix/source/lattice_armv7.S',
            'fix/source/pitch_filter_armv6.S',
          ],
          'sources!': [
            'fix/source/lattice_c.c',
            'fix/source/pitch_filter_c.c',
          ],
          'conditions': [
            ['arm_neon==1 or arm_neon_optional==1', {
              'dependencies': [ 'isac_neon' ],
            }],
          ],
        }],
        ['target_arch=="arm64"', {
          'dependencies': ['isac_neon', ],
        }],
        ['target_arch=="mipsel" and mips_arch_variant!="r6"', {
          'sources': [
            'fix/source/entropy_coding_mips.c',
            'fix/source/filters_mips.c',
            'fix/source/lattice_mips.c',
            'fix/source/pitch_estimator_mips.c',
            'fix/source/transform_mips.c',
          ],
          'sources!': [
            'fix/source/lattice_c.c',
            'fix/source/pitch_estimator_c.c',
          ],
          'conditions': [
            ['mips_dsp_rev>0', {
              'sources': [
                'fix/source/filterbanks_mips.c',
              ],
            }],
            ['mips_dsp_rev>1', {
              'sources': [
                'fix/source/lpc_masking_model_mips.c',
                'fix/source/pitch_filter_mips.c',
              ],
              'sources!': [
                'fix/source/pitch_filter_c.c',
              ],
            }],
          ],
        }],
      ],
    },
  ],
  'conditions': [
    ['(target_arch=="arm" and arm_version>=7) or target_arch=="arm64" or target_arch=="arm64" or winrt_platform=="win_phone" or winrt_platform=="win10_arm"', {
      'targets': [
        {
          'target_name': 'isac_neon',
          'type': 'static_library',
          'includes': ['../../../../build/arm_neon.gypi',],
          'dependencies': [
            '<(webrtc_root)/common_audio/common_audio.gyp:common_audio',
          ],
          'sources': [
            'fix/source/entropy_coding_neon.c',
            'fix/source/filters_neon.c',
            'fix/source/lattice_neon.c',
            'fix/source/transform_neon.c',
          ],
          'conditions': [
            # Disable LTO in isac_neon target due to compiler bug
            ['use_lto==1', {
              'cflags!': [
                '-flto',
                '-ffat-lto-objects',
              ],
            }],
          ['winrt_platform=="win_phone" or winrt_platform=="win10_arm"', {
            'rules': [
            {
              'rule_name': 'gas_preprocessor',
              'extension': 'S',
              'inputs': [
               ],
               'outputs': [
                 '<(INTERMEDIATE_DIR)/<(RULE_INPUT_ROOT).obj',
               ],
               'action': [
                 'perl ../build/gas-preprocessor/gas-preprocessor.pl -as-type armasm -force-thumb -- armasm -oldit -I../../ -c <(RULE_INPUT_PATH) -o <(INTERMEDIATE_DIR)/<(RULE_INPUT_ROOT).obj'
               ],
               'process_outputs_as_sources': 0,
               'message': 'Compiling <(RULE_INPUT_PATH)',
             }],
            }],
            # Disable AllpassFilter2FixDec16Neon function due to a clang
            # bug. Refer more details at:
            # https://code.google.com/p/webrtc/issues/detail?id=4567
            ['target_arch!="arm64" or clang==0', {
                  'sources': ['fix/source/filterbanks_neon.c',],
            }]
          ],
        },
      ],
    }],
  ],
}
