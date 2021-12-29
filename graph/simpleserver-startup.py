import http.server as server


def main():
    from matplotlib import pyplot as pyp

    x = [1, 3, 5, 30, 55, 100]
    y = range(len(x))
    x2 = [3, 5, 10, 29, 50, 120]
    pyp.title("Matplotlib Graph", {"fontsize": 25})
    pyp.xlabel("x-number", {"fontsize": 15})
    pyp.ylabel("y-number", {"fontsize": 15})
    pyp.plot(x, y, label='graph1')
    pyp.plot(x2, y, label='graph2')
    pyp.legend()
    pyp.show()
    pyp.savefig('picture.png')


if __name__ == '__main__':
    server.test(HandlerClass=server.CGIHTTPRequestHandler)
    main()
