from collections import OrderedDict

def to_sens(text):
    """(4.1.1) splits a text into sentences
    (on ".", "!", "?", etc.)"""
    sens = []
    for piece1 in text.split('.'):
        for piece2 in piece1.split('!'):
            for piece3 in piece2.split('?'):
                if piece3:
                    sens.append(piece3)
    return sens


def to_sens2(szoveg):
    """(4.1.1) another solution """
    mondatok = []
    for punct in ".?":
        szoveg = szoveg.strip().replace(punct, '!')
    for mondat in szoveg.split('!'):
        if mondat.strip():
            mondatok.append(mondat.strip())
    return mondatok


def test_to_sens():
    szoveg = open('data/sample_text.txt').read()
    print(mondatokra(szoveg)[-3:])


def szavakra(mondat):
    """splits sentences into words, and strips punctuation
    marks (",", ";", etc.) from edges of words."""
    szavak = mondat.split()
    strippelt_szavak = []
    for szo in szavak:
        strippelt_szavak.append(szo.strip(",;:()"))
    return strippelt_szavak



def feldolgoz(fajl):
    """takes a filename as its argument and returns the text
    in the file as a list of lists."""
    kimenet = []
    szoveg = open(fajl).read()
    for mondat in mondatokra(szoveg):
        szavak = szavakra(mondat)
        kimenet.append(szavak)
    return kimenet


def test_process():
    """test the function feldolgoz on data/sample_text.txt"""
    adat = feldolgoz('data/sample_text.txt')
    print(adat[:3])



def joe(fajl):
    """goes through a text and replaces all proper names
    (capitalized words not at the beginning of a sentence)
    with "Joe"."""
    kimenet = []
    adat = feldolgoz(fajl)
    for mondat in adat:
        uj_mondat = []
        uj_mondat.append(mondat[0])
        for szo in mondat[1:]:
            if szo.istitle():
                uj_mondat.append("Joe")
            else:
                uj_mondat.append(szo)
        kimenet.append(uj_mondat)
    return kimenet
            


def test_joe():
    """Print the first few sentences to test your solution."""
    joe('data/sample_text.txt')[-3:]




def is_symmetric(matrix):
    """Define a function that takes as its input a list of $n$
    lists of $n$ numbers (a square matrix) and decides if it is
    symmetric (i.e. $A[i,j] == A[j,i]$ for all $i, j$)."""
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            if matrix[i][j] != matrix[j][i]:
                return False
    return True


def test_symm():
    """test the func is_symmteric"""
    test_matrix1 = [[1,2], [3,4]]
    test_matrix2 = [[1,2], [2,1]]
    print is_symmetric(test_matrix1)
    print is_symmetric(test_matrix2)





def transpose(matrix):
    """takes a list containing lists of equal length (i.e. a table
    of size $n\times k$) and "transposes" it, creating a table of
    size $k\times n$."""
    n = len(matrix)
    k = len(matrix[0])
    new_matrix = []
    for i in range(k):
        new_row = []
        for old_row in matrix:
            new_row.append(old_row[i])
        new_matrix.append(new_row)
    return new_matrix
    




def transpose2(matrix):
    """redoing 4.2.3 using nested list comprehension!"""
    n = len(matrix)
    m = len(matrix[0])
    return [[matrix[i][j] for i in range(n)] for j in range(m)]


def test_transpose():
    """testing transpose function"""
    test_matrix = [[1,2,3], [4,5,6]]
    print(transpose(test_matrix))



def process_data(fn):
    """Read a movie datafile and store it in a dictionary whose
    keys are genres and the values are list of tuples of title and year"""
    data = {}
    f = open(fn)
    for line in f:
        title, year, genres = line.strip().split('\t')
        title = title.strip()
        year = int(year)
        genres = genres.split(",")
        for genre in genres:
            if genre not in data:
                data[genre] = []
            data[genre].append((title, year))
    return data        


def test_movie_proc():
    """Test the process_data function on data/movies.tsv"""
    data = process_data("data/movies.tsv")
    print(data['horror'][:5])


def build_index(data):
    """buld index for incremental search"""
    letter_index = {}
    for movie in data:
        title = movie[0]
        try:
            a, b, c = title[:3]
        except ValueError:
            print "skipping: {0}".format(title)
            continue
        if a not in letter_index:
            letter_index[a] = {}
        if b not in letter_index[a]:
            letter_index[a][b] = {}
        if c not in letter_index[a][b]:
            letter_index[a][b][c] = []
        letter_index[a][b][c].append(movie)
    return letter_index


def search(fn):
    """an incremental search of movie titles: users should be
    able to narrow the set of movies with every character they type."""
    data = [(title.strip(), int(year), genres.split(','))
            for title, year, genres in [line.strip().split('\t')
                                        for line in open(fn)]]
    letter_index = build_index(data)
    letter1 = raw_input()
    print letter_index[letter1]
    letter2 = raw_input()
    print letter_index[letter1][letter2]
    letter3 = raw_input()
    print letter_index[letter1][letter2][letter3]




def query():
    last_name = raw_input()
    first_name = raw_input()
    year = int(raw_input())
    hobby = raw_input()
    return last_name, first_name, year, hobby


def query_users():
    """Queries users for their last name, first name,
    year of birth, and hobby, and populates an OrderedDict
    whose keys are the last names and values are dictionaries
    with four keys each. If a second person with the same last
    name is encountered, both should now have keys of the form
    "lastname_firstname". If the same person is encountered multiple
    times, his/her data should be updated."""
    data = OrderedDict()
    while True:
        last_name, first_name, year, hobby = query()
        full_name = "{0}_{1}".format(last_name, first_name)
        if last_name not in data:
            if full_name in data:
                data[full_name] = (first_name, year, hobby)
            else:
                data[last_name] = (first_name, year, hobby)
                 
        else:
            data[full_name] = (first_name, year, hobby)
            first_guy = data[last_name]
            first_key = "{0}_{1}".format(last_name, first_guy[0])
            data[first_key] = first_guy
            del data[last_name]
        print data
