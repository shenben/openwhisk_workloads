import helper
def main(args):
    name = args.get("name", "stranger")
    stat = helper.ok()
    greeting = "Hello " + name + "!" + str(stat)
    print(greeting)
    return {"greeting": greeting}
