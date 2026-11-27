#!/usr/bin/env -S PYTHONPATH=../../../tools/extract-utils python3
#
# SPDX-FileCopyrightText: 2025 The LineageOS Project
# SPDX-License-Identifier: Apache-2.0
#

from extract_utils.fixups_blob import (
    blob_fixup,
    blob_fixups_user_type,
)
from extract_utils.fixups_lib import (
    lib_fixups,
    lib_fixups_user_type,
)
from extract_utils.main import (
    ExtractUtils,
    ExtractUtilsModule,
)


namespace_imports = [
    'device/samsung/sm7325-common',
    'hardware/qcom-caf/sm8350',
    'hardware/qcom-caf/wlan',
    'hardware/samsung',
    'vendor/qcom/opensource/dataservices',
    'vendor/qcom/opensource/display',
]

lib_fixups: lib_fixups_user_type = {
    **lib_fixups,
}

blob_fixups: blob_fixups_user_type = {
    'vendor/lib64/libsec-ril.so': blob_fixup()
        .binary_regex_replace(b'ril.dds.call.ongoing', b'vendor.calls.slot_id')
        # Android U+ rejects Samsung's quoted SMSC format for IMS SMS.
        .sig_replace(
            '60 0e 40 f9 82 0c 80 52 24 00 80 52 e1 03 15 aa 08 00 40 f9 03 00 80 d2',
            '60 0e 40 f9 82 0c 80 52 24 00 80 52 e1 03 15 aa 08 00 40 f9 e3 03 14 aa'
        )
        .sig_replace(
            '68 16 40 f9 aa c3 01 d1 eb 03 00 91 00 e4 00 6f '
            'a8 83 1f f8 e8 03 80 92 a9 83 00 91 08 f0 df f2 '
            '4a 81 00 91 6b 01 02 91 a0 83 3e ad a9 2b 3d a9 '
            'ab 23 3e a9 a0 87 7e ad 82 ed ff d0 42 64 2c 91 '
            'a3 43 01 d1 c1 03 80 52 a0 87 3d ad 55 94 07 94',
            '68 16 40 f9 a8 83 1f f8 a8 c3 01 d1 a3 43 01 d1 '
            '68 7c 00 a9 7f 7c 01 a9 29 a4 ff 10 df 03 09 eb '
            '82 ed ff d0 42 64 2c 91 01 01 00 54 c2 00 00 10 '
            '88 00 40 39 bf 44 02 71 04 09 40 7a 42 14 82 9a '
            '02 00 00 14 2b 25 73 00 c1 03 80 52 55 94 07 94'
        )
        # Always emit uiccApplicationsEnablementChanged.
        .sig_replace('88 58 9D 52 1F 00 08 6B AB 01 00 54', '88 58 9D 52 1F 00 08 6B 1F 20 03 D5')
        .sig_replace('88 58 9D 52 FF 02 08 6B AB 01 00 54', '88 58 9D 52 FF 02 08 6B 1F 20 03 D5'),
    ('vendor/lib64/hw/gatekeeper.mdfpp.so', 'vendor/lib64/libkeymaster_helper.so', 'vendor/lib64/libskeymaster4device.so'): blob_fixup()
        .replace_needed('libcrypto.so', 'libcrypto-v33.so'),
    ('vendor/lib/libdpps.so', 'vendor/lib64/libdpps.so', 'vendor/lib/libsnapdragoncolor-manager.so', 'vendor/lib64/libsnapdragoncolor-manager.so'): blob_fixup()
        .replace_needed('libtinyxml2.so', 'libtinyxml2-v34.so'),
    ('vendor/lib/libwvhidl.so', 'vendor/lib/mediadrm/libwvdrmengine.so'): blob_fixup()
        .add_needed('libcrypto_shim.so'),
    ('vendor/lib/unihal_main@2.15.so', 'vendor/lib64/unihal_main@2.15.so'): blob_fixup()
        .add_needed('libui_shim.so'),
}  # fmt: skip

module = ExtractUtilsModule(
    'sm7325-common',
    'samsung',
    blob_fixups=blob_fixups,
    lib_fixups=lib_fixups,
    namespace_imports=namespace_imports,
)

if __name__ == '__main__':
    utils = ExtractUtils.device(module)
    utils.run()
