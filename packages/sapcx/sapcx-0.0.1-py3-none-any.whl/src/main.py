import sys

import src.api as api
import src.cli as cli
from src.console import flexiblesearch
from src.console import scripting
from src.console import impex


def main():
    if len(sys.argv) <= 1:
        cli.cli.print_usage()
        exit(1)

    args = cli.cli.parse_args()

    api_client = api.SAPAPI(username=args.username, password=args.password, hacurl=args.server)
    api_client.login()

    impex_console = impex.ImpexEngine(api_client)
    scripting_console = scripting.Scripting(api_client)
    flexiblesearch_console = flexiblesearch.FlexibleSearch(api_client)

    if args.import_impex:
        file = args.import_impex
        impex_script = impex.Impex(file, is_file=True)
        result = impex_console.impex_import(impex_script)
        if result.is_ok():
            print(f"Impex {file} executed successfully")
        else:
            print(result.get_errors())
            exit(2)

    if args.execute_groovy:
        file = args.execute_groovy
        script = scripting.Script(file, is_file=True)
        result = scripting_console.execute(script)
        if result.is_ok():
            print(result.output)
        else:
            print(result.get_errors())
            exit(2)

    if args.query:
        query = args.query
        result = flexiblesearch_console.execute(query)
        if result.is_ok():
            print(result.get_result())
        else:
            print(result.get_errors())
            exit(2)
