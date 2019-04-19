from itertools import zip_longest


def text_span(txt):
    txt = ">{txt}</tspan>".format(txt=txt)
    return txt


def text_char_replace(txt):
    char_map = {
        'ť': 't',
        'ď': 'd',
    }
    replaced = []
    for old, new in char_map.items():
        if old in txt:
            replaced.append(old)
        txt = txt.replace(old, new)

    return txt, replaced


def save_renamed(fname, base_svg, texts, wanted):
    assert len(texts) == len(wanted)

    print('>>> Generating and saving {fname}'.format(fname=fname))

    all_replaced = []
    for text, want in zip(texts, wanted):
        want_orig = want
        want, replaced = text_char_replace(want)

        if replaced:
            txt = (
                '! These characters {chars}, were replaced in {old} - producing {new}'
                ' - be sure to add diacritics manually.'
            )
            print(txt.format(
                old=want_orig,
                new=want,
                chars=replaced,
            ))
            all_replaced.append(replaced)

        text = text_span(text)
        want = text_span(want)
        base_svg = base_svg.replace(text, want)

    with open(fname, 'w') as fil:
        fil.write(base_svg)


def load_base(fname):
    with open(fname, 'r') as fil:
        txt = fil.read()
    return txt


def load_names(fname):
    with open(fname, 'r') as fil:
        lines = fil.readlines()

    lines = [line.strip() for line in lines if line.strip()]
    return lines

# t' a d'
# fida peta, vita


def grouper(n, iterable, padvalue=None):
    """Group iterable in lists with length n.

    grouper(3, 'abcdefg', 'x') --> ('a','b','c'), ('d','e','f'), ('g','x','x')
    """
    return zip_longest(*[iter(iterable)] * n, fillvalue=padvalue)


if __name__ == "__main__":

    fname_names = 'names.txt'
    names = load_names(fname_names)

    fname_base = 'base.svg'
    base_svg = load_base(fname_base)

    group_len = 4
    texts = ['name_here_{num}'.format(num=num) for num in range(group_len)]

    for index, wanted in enumerate(grouper(group_len, names, '')):
        fname_new = 'out/generated_{index}.svg'.format(index=index)
        save_renamed(fname_new, base_svg, texts, wanted)
