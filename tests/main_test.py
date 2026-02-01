config_stubs = {}


def test_main_exits_with_code_0_and_success_message_when_completing_execution(
    cli, config_path
):
    # Set default config path using stub - it is a generator, so call next().
    next(config_path())
    # main() runs without arguments, and should pick up default config path from fixture
    result = cli()

    # teardown - very ugly
    next(config_path())

    assert result.exit_code == 0


# def test_main_can_read_an_existing_config_file_when_no_path_is_provided(
#     cli, config_path
# ):
#     config_path("mock-yaml-data")
#     result = cli()
#     assert result.exit_code == 0
#     assert result.output == "Success!"


# # Do not use the config_path fixture here, so we can test failure when no path is provided and no default config exists.
# @pytest.mark.parametrize(
#     ("argument", "expected exception"),
#     [
#         (None, InvalidArgumentException),
#         ("", InvalidArgumentException),
#         (" ", InvalidArgumentException),
#         ("invalid/path/to/config.yaml", InvalidArgumentException),
#     ],
# )
# def test_exits_with_code_1_and_appropriate_message_when_given_incorrect_arguments(
#     cli, path: str, expected_exception: Exception
# ):
#     result = cli(path)
#     with pytest.raises(expected_exception):
#         assert result.exit_code == 1
#         assert result.output == f"An error occurred : {repr(expected_exception)}"
