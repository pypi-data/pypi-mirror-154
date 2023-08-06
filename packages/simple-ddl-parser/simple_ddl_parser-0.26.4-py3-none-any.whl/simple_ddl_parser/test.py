from simple_ddl_parser import DDLParser

ddl = """create temp table tempevent(like event);

"""

result = DDLParser(ddl).run(group_by_type=True)

import pprint
pprint.pprint(result) 
