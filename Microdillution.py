def get_values(*names):
    import json
    _all_values = json.loads("""{"number_of_samples":96,"right_pipette":"p300_multi_gen2","left_pipette":"p1000_single_gen2","media_volume":100,"DNA_volume":2}""")
    return [_all_values[n] for n in names]

import math

metadata = {
    'protocolName': 'Microdillution',
    'author': 'Gabriel Cabot, phD <gabriel.cabot@ssib.es>',
    'source': 'ARBPIG / MLS (IdISBa)',
    'apiLevel': '2.2'
    }


def run(protocol_context):
    [number_of_samples, left_pipette, right_pipette, media_volume,
     DNA_volume] = get_values(  # noqa: F821
        "number_of_samples", "left_pipette", "right_pipette",
        "media_volume", "DNA_volume"
     )
    solution_media_volume=897
    solution_ATB_volume=103
    transfer_volume=100
    num_dilutions=10

    if not left_pipette and not right_pipette:
        raise Exception('You have to select at least 1 pipette.')

    pipette_l = None
    pipette_r = None

    for pip, mount, slots in zip(
            [left_pipette, right_pipette],  #Which pipettes are mounted (Described in JSON)
            ['left', 'right'],              #Where pipettes are mounted
            [['10'], ['11']]):              #Where tippracks for each pipette are located

        if pip:
            range = pip.split('_')[0][1:]
            rack = 'opentrons_96_tiprack_' + range + 'ul'
            tipracks = [
                protocol_context.load_labware(rack, slot) for slot in slots]
            if mount == 'left':
                pipette_l = protocol_context.load_instrument(
                    pip, mount, tip_racks=tipracks)
            else:
                pipette_r = protocol_context.load_instrument(
                    pip, mount, tip_racks=tipracks)

    # labware setup - set names, types, positions, and descriptions of all labware
    dest_plate1 = protocol_context.load_labware(
        'opentrons_96_wellplate_200ul_pcr_full_skirt', '1', 'Output plate 1')
    dest_plate2 = protocol_context.load_labware(
        'opentrons_96_wellplate_200ul_pcr_full_skirt', '2', 'Output plate 2')
    dest_plate4 = protocol_context.load_labware(
        'opentrons_96_wellplate_200ul_pcr_full_skirt', '4', 'Output plate 4')
    dest_plate5 = protocol_context.load_labware(
        'opentrons_96_wellplate_200ul_pcr_full_skirt', '5', 'Output plate 5')
    dest_plate7 = protocol_context.load_labware(
        'opentrons_96_wellplate_200ul_pcr_full_skirt', '7', 'Output plate 7')
    dest_plate8 = protocol_context.load_labware(
        'opentrons_96_wellplate_200ul_pcr_full_skirt', '8', 'Output plate 8')
    med_res = protocol_context.load_labware(
        'nest_1_reservoir_290ml', '3', 'Media reservoir')
    temp_mod = protocol_context.load_module('temperature module gen2', '6')
    temp_block = temp_mod.load_labware(
                    'opentrons_24_aluminumblock_generic_2ml_screwcap')

    # Wells
    ATB_1 = temp_block['A1']
    ATB_2 = temp_block['B1']
    ATB_3 = temp_block['C1']
    trash = protocol_context.fixed_trash
    destemp_block = [temp_block['A2'],temp_block['A3'],temp_block['B2']]

    # determine which pipette has the smaller volume range
    if pipette_l and pipette_r:
        if left_pipette == right_pipette:
            pip_s = pipette_l
            pip_l = pipette_r
        else:
            if pipette_l.max_volume < pipette_r.max_volume:
                pip_s, pip_l = pipette_l, pipette_r
            else:
                pip_s, pip_l = pipette_r, pipette_l
    else:
        pipette = pipette_l if pipette_l else pipette_r

    # reagent setup
    media = med_res.wells()[0]
    col_num = math.ceil(number_of_samples/8)
#    temp_mod.set_temperature(celsius=14)

    # distribute media
    if pipette_l and pipette_r:
        if media_volume <= pip_s.max_volume:
            pipette = pip_s
        else:
            pipette = pip_l
    pipette.pick_up_tip()
    for dest in dest_plate1.rows()[0][:col_num]:
        pipette.transfer(
            media_volume,
            media,
            dest,
            new_tip='never'
        )
    pipette.transfer(
        media_volume,
        media,
        dest_plate1.rows()[0][:11],
        new_tip='never'
    )
    for dest in dest_plate2.rows()[0][:col_num]:
        pipette.transfer(
            media_volume,
            media,
            dest,
            new_tip='never'
        )
    pipette.transfer(
        media_volume,
        media,
        dest_plate2.rows()[0][:11],
        new_tip='never'
    )
    for dest in dest_plate4.rows()[0][:col_num]:
        pipette.transfer(
            media_volume,
            media,
            dest,
            new_tip='never'
        )
    pipette.transfer(
        media_volume,
        media,
        dest_plate4.rows()[0][:11],
        new_tip='never'
    )
    for dest in dest_plate5.rows()[0][:col_num]:
        pipette.transfer(
            media_volume,
            media,
            dest,
            new_tip='never'
        )
    pipette.transfer(
        media_volume,
        media,
        dest_plate5.rows()[0][:11],
        new_tip='never'
    )
    for dest in dest_plate7.rows()[0][:col_num]:
        pipette.transfer(
            media_volume,
            media,
            dest,
            new_tip='never'
        )
    pipette.transfer(
        media_volume,
        media,
        dest_plate7.rows()[0][:11],
        new_tip='never'
    )
    for dest in dest_plate8.rows()[0][:col_num]:
        pipette.transfer(
            media_volume,
            media,
            dest,
            new_tip='never'
        )
    pipette.transfer(
        media_volume,
        media,
        dest_plate8.rows()[0][:11],
        new_tip='never'
    )
    pipette.blow_out(media.top())
    pipette.drop_tip()

    # prepare ATB solution
#    if pipette_l and pipette_r:
#        if solution_media_volume <= pip_s.max_volume:
#            pipette = pip_s
#        else:
#            pipette = pip_l

    pipette = pip_l
    pipette.pick_up_tip()
    for dest in [temp_block['A2'],temp_block['A3'],temp_block['B2'],temp_block['B3'],temp_block['C2'],temp_block['C3']]:
        pipette.transfer(
            solution_media_volume,
            media,
            dest,
            new_tip='never'            
        )
    pipette.drop_tip()

    pipette = pip_l
#    pipette.pick_up_tip()
    for dest in [temp_block['A2'],temp_block['B2'],temp_block['C2'],temp_block['A3'],temp_block['B3'],temp_block['C3']]:
        pipette.transfer(
            solution_ATB_volume,
            temp_block['A1'],
            dest,
            mix_before=(3,100)
        )
#    pipette.drop_tip()

    # Load ATB on plates
    pipette = pip_l
    for dest in [dest_plate1['A1'],dest_plate1['B1'],dest_plate1['C1'],dest_plate1['D1'],dest_plate1['E1'],dest_plate1['F1'],dest_plate1['G1'],dest_plate1['H1']]:
        pipette.transfer(
            transfer_volume,
            temp_block['A2'],
            dest,
            mix_before=(3, 100)
            )

    for dest in [dest_plate2['A1'],dest_plate2['B1'],dest_plate2['C1'],dest_plate2['D1'],dest_plate2['E1'],dest_plate2['F1'],dest_plate2['G1'],dest_plate2['H1']]:
        pipette.transfer(
            transfer_volume,
            temp_block['B2'],
            dest,
            mix_before=(3, 100)
            )

    for dest in [dest_plate4['A1'],dest_plate4['B1'],dest_plate4['C1'],dest_plate4['D1'],dest_plate4['E1'],dest_plate4['F1'],dest_plate4['G1'],dest_plate4['H1']]:
        pipette.transfer(
            transfer_volume,
            temp_block['C2'],
            dest,
            mix_before=(3, 100)
            )

    for dest in [dest_plate5['A1'],dest_plate5['B1'],dest_plate5['C1'],dest_plate5['D1'],dest_plate5['E1'],dest_plate5['F1'],dest_plate5['G1'],dest_plate5['H1']]:
        pipette.transfer(
            transfer_volume,
            temp_block['A3'],
            dest,
            mix_before=(3, 100)
            )

    for dest in [dest_plate7['A1'],dest_plate7['B1'],dest_plate7['C1'],dest_plate7['D1'],dest_plate7['E1'],dest_plate7['F1'],dest_plate7['G1'],dest_plate7['H1']]:
        pipette.transfer(
            transfer_volume,
            temp_block['B3'],
            dest,
            mix_before=(3, 100)
            )

    for dest in [dest_plate8['A1'],dest_plate8['B1'],dest_plate8['C1'],dest_plate8['D1'],dest_plate8['E1'],dest_plate8['F1'],dest_plate8['G1'],dest_plate8['H1']]:
        pipette.transfer(
            transfer_volume,
            temp_block['C3'],
            dest,
            mix_before=(3, 100)
            )

    # Mix plates
    pipette = pip_s
    for dest in [dest_plate1]:
        row = dest.rows()[0]
        pipette.transfer(
            100,
            row[:num_dilutions-1],
            row[1:num_dilutions],
            mix_before=(3, 50)
        )