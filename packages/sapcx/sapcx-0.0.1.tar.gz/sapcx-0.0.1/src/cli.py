#!/usr/bin/env python3

import argparse

cli = argparse.ArgumentParser()

cli.add_argument('-i', '--import', help='Impex file to import', dest='import_impex')
cli.add_argument('-e', '--execute', help="Groovy script file to execute", dest='execute_groovy')
cli.add_argument('-q', '--query', help="Run flexible search query", dest='query')


server_group = cli.add_argument_group('server')
server_group.add_argument('-u', '--username', default='admin')
server_group.add_argument('-p', '--password', default='nimda')
server_group.add_argument('-s', '--server', default='https://localhost:9002')
