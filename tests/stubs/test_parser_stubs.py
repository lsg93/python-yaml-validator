valid_yaml_str = """
        application:
            name: MyAwesomeApp
            version: "1.0.0"
            debug_mode: true
        database:
            type: postgresql
            host: localhost
            port: 5432
            credentials:
                username: admin
                password: secretpassword
        settings:
            threshold: 0.85
            timeout_seconds: 30
            features:
                - user_profiles
                - notifications
                - dark_mode
        """

valid_yaml_stub = {
    "input": valid_yaml_str,
    "expected_result": {
        "application": {"name": "MyAwesomeApp", "version": "1.0.0", "debug_mode": True},
        "database": {
            "type": "postgresql",
            "host": "localhost",
            "port": 5432,
            "credentials": {"username": "admin", "password": "secretpassword"},
        },
        "settings": {
            "threshold": 0.85,
            "timeout_seconds": 30,
            "features": ["user_profiles", "notifications", "dark_mode"],
        },
    },
}

malformed_yaml_stub = """
        application:
          name: MyAwesomeApp
          version "1.0.0" # Missing colon here
             debug_mode: true # Incorrect indentation
        """

empty_yaml_stub = ""

incorrectly_nested_yaml_stub = """
        level1:
          level2:
         level3: value # Incorrectly indented
        """

multiple_documents_yaml_stub = """
        # Document 1
        config:
            name: PrimaryConfig
            enabled: true
        ---
        # Document 2
        server:
            port: 8080
            host: 127.0.0.1
        ---
        # Document 3
        database:
            type: sqlite
            path: /var/data/app.db
        """
