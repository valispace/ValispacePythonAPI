import valispace
import asyncio

PROJECT = 26

def main():
    vs = valispace.Valispace("http://127.0.0.1:8000", "admin2", "12345678", options={
        "project": PROJECT,
    })

    valis = vs.get_valis()
    print(valis)


main()
