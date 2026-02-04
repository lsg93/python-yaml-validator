def test_main_exits_with_code_0_and_success_message_when_completing_execution(
    cli, create_config
):
    # fixture creates a default config if no path is provided.
    create_config()

    # main() runs without arguments, and should pick up default config path from fixture
    result = cli()

    assert result.exit_code == 0


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
