import argparse
import fizz_engine

from flask import Flask, jsonify, g
app = Flask(__name__)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def fizz(path):
    if not path:
        return ''
    result = {"path": path, "errors": [], "data": None}
    if "//" in path:
        result["warnings"] = ["Empty terms found in path."]
    arguments = path.split('/')
    try:
        size = int(arguments.pop())
    except ValueError:
        result["errors"].append("Invalid size as final path term.")
    if not arguments:
        result["errors"].append("No replacement terms provided in path.")
    if not result["errors"]:
        try:
            fizz = fizz_engine.fizz_factory(app.config["MAX_TERMS"])
            result["data"] = list(fizz.get_fizz(size, words=arguments))
        except ValueError:
            result["errors"].append(("Too Many Terms:  Request of %d temrs "
                                     "exceeds the maximum of %d") % (
                                         len(arguments), g.fizz.max_size))
    return jsonify(result)

def main():
    parser = argparse.ArgumentParser(
        description="A network server to deliver Fizz Buzz sequences")
    parser.add_argument("--max_terms", metavar="N", type=int, default=256,
                        help="Maximum number of replacement terms to support.")
    parser.add_argument("--host", type=str,
                        help="Interface to bind the server socket to.")
    parser.add_argument("--port", type=int, default=8081,
                        help="Port to bind the server socket to.")
    parser.add_argument("--debug", default=False, action="store_true",
                        help="Run the server in debug mode")
    args = parser.parse_args()

    # Prime the cache with the created FizzEngine
    fizz_engine.fizz_factory(args.max_terms)
    with app.app_context():
        app.config["MAX_TERMS"] = args.max_terms

    app.run(port=args.port, host=args.host, debug=args.debug)


if __name__ == '__main__':
    main()
