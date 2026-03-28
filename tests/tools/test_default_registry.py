from code_agent.tools.default_registry import create_default_registry


class TestDefaultRegistry:
    def test_all_tools_registered(self) -> None:
        registry = create_default_registry()
        expected_tools = [
            "glob",
            "read_file",
            "write_file",
            "replace",
            "list_directory",
            "grep_search",
            "web_fetch",
            "run_shell_command",
        ]
        for name in expected_tools:
            assert registry.get_tool(name) is not None, f"Tool '{name}' not registered"

    def test_declarations_count(self) -> None:
        registry = create_default_registry()
        declarations = registry.get_declarations()
        assert len(declarations) == 8
