
import yaml

def is_in_file( str: str, filename: str ) -> bool:
    with open( filename, 'r' ) as fp:
        for l_no, line in enumerate( fp ):
            if str in line:
                return True
    return False

def count_in_file( str: str, filename: str ) -> int:
    n = 0
    with open( filename, 'r' ) as fp:
        for l_no, line in enumerate( fp ):
            if str in line:
                n += 1
    return n

def load_yaml( filename: str ) -> dict:
    file = open( filename, 'r' )
    result = yaml.safe_load( file )
    file.close()
    return result

def save_yaml( filename: str, yaml_dict: str ):
    with open( filename, 'w' ) as file: yaml.dump( yaml_dict, file )

# def has_evaluation(chart_dict, eval_key):
#     if eval_key in chart_dict and "score" in chart_dict[eval_key] and chart_dict[eval_key]["score"] != "":
#         return True
#     return False
