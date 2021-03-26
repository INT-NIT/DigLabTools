from redcap_bridge.project_building import build_project, customize_project


def test_


    print('Running V4A project build, customization and upload')


    build_project('../projects/V4A/V4A_structure.csv', 'tmp_V4A.csv')
    customize_project('tmp_V4A.csv', '../projects/V4A/V4A_customizations.csv',
                      output_file='tmp_V4A_custom.csv')

    upload_datadict('tmp_V4A_custom.csv',
                    '../projects/V4A/redcap_server_config.json')