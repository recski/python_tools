"""incremental search in movie database"""

def unify_dicts(dict1, dict2):
    dict3 = {}
    dict3.update(dict1)
    for key, value in dict2.items():
        if key not in dict3:
            dict3[key] = value
        else:
            if not isinstance(dict3[key], dict):
                dict3[key] = value
            else:
                dict3[key] = unify_dicts(dict3[key], value)
    return dict3


def get_letter_dict(title, movie):
    if not title:
        return {'@': movie}
    else:
        return {title[0]: get_letter_dict(title[1:], movie)}


def build_index(data):
    letter_index = {}
    for movie in data:
        title = movie[0]
        d = get_letter_dict(title, movie)
        letter_index = unify_dicts(letter_index, d)
    return letter_index


def search(fn):
    data = [(title.strip(), int(year), genres.split(','))
            for title, year, genres in [line.strip().split('\t')
                                        for line in open(fn)]]
    
    letter_index = build_index(data)
    letter = raw_input()
    curr_dict = letter_index[letter]
    while True:
        print curr_dict
        if '@' in curr_dict:
            print curr_dict['@']
            break
        else:
            letter = raw_input()
            if letter not in curr_dict:
                print 'not found :('
                break
            curr_dict = curr_dict[letter]
        
if __name__ == "__main__":
    search("data/movies.tsv")
