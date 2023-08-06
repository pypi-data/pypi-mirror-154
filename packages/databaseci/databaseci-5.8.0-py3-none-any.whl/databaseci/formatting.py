def format_table_of_dicts(t):
    if not t:
        return "Empty table."

    klist = list(t[0].keys())

    ttt = [str(type(_).__name__) for _ in t[0].values()]

    st = [{k: str(v) for k, v in r.items()} for r in t]

    st.insert(0, {k: k for k in klist})

    w = {_: 0 for _ in klist}

    for r in st:
        for kk in klist:
            l = len(r[kk])
            if w[kk] < l:
                w[kk] = l

    st.insert(1, {k: "-" * w[k] for k in w})

    for r in st:
        for tt, kk in zip(ttt, klist):
            ww = w[kk]

            s = r[kk]

            if tt == "str":
                r[kk] = s.ljust(ww)

            else:
                r[kk] = s.rjust(ww)

    return "\n".join(" ".join(x.values()) for x in st)
