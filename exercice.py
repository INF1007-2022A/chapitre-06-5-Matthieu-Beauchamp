#!/usr/bin/env python
# -*- coding: utf-8 -*-


# The teacher's method is way more elegant
def check_brackets(text, brackets: list):
    # helper functions on brackets indices / Ids
    def isOpen(x): return x % 2 == 0
    def isClose(x): return x % 2 != 0

    bracketIds = [brackets.index(bracket) for bracket in text
                  if bracket in brackets]

    start = 0  # cache position for later cycles
    while len(bracketIds) > 0:
        for i in range(start, len(bracketIds)):
            closeId = bracketIds[i]
            if isClose(closeId):
                if i == 0:
                    return False

                expectedOpenId = bracketIds[i-1]
                if expectedOpenId != closeId - 1:  # no match
                    return False
                else:  # matched, remove them (i-1, i), and set start
                    bracketIds = bracketIds[0:i-1] + bracketIds[i+1:]
                    start = i-1
                    break

            elif i == len(bracketIds)-1:  # Never closes
                return False

    return True


def remove_comments(full_text, comment_start, comment_end):
    while True:
        startPos = full_text.find(comment_start)
        endPos = full_text.find(comment_end)

        if startPos == -1 and endPos == -1:
            return full_text

        oneIsMissing = startPos == -1 or endPos == -1
        areInWrongOrder = endPos < startPos

        if oneIsMissing or areInWrongOrder:
            return None

        full_text = full_text[:startPos]\
            + full_text[endPos+len(comment_end):]


def get_tag_prefix(text, opening_tags, closing_tags):
    for tag in opening_tags:
        if text.find(tag) == 0:
            return (tag, None)

    for tag in closing_tags:
        if text.find(tag) == 0:
            return (None, tag)

    return (None, None)


def nextTagPos(txt, tag_names, start=0):
    """Returns (position, tag_name, status)
    where status: -1 -> invalid
                   0 -> open
                   1 -> close
    or None if there is not tags after start
    """
    if len(tag_names) == 0:
        return None

    minPos = txt.find(tag_names[0], start)
    closestTag = tag_names[0]
    for tag in tag_names:
        pos = txt.find(tag, start)
        if pos != -1 and pos < minPos:
            closestTag = tag
            minPos = pos

    if minPos == -1:
        return None

    status = -1
    if txt[minPos+len(closestTag)] == '>':
        if txt[minPos-1] == "<":
            status = 0

        if txt[minPos-2:minPos] == "</":
            status = 1

    return minPos, closestTag, status


def check_tags(full_text, tag_names, comment_tags):
    def getNextTagFromReport(tagReport):
        return nextTagPos(full_text, tag_names,
                          tagReport[0] + len(tagReport[1]))

    full_text = remove_comments(full_text,
                                comment_tags[0],
                                comment_tags[1])

    if full_text is None:
        return False

    tagStack = []
    tagReport = nextTagPos(full_text, tag_names)
    while tagReport is not None:
        # For invalid reports, we just go next

        if tagReport[2] == 0:
            tagStack.append(tagReport[1])

        elif tagReport[2] == 1:
            if len(tagStack) == 0:
                return False
            if tagReport[1] != tagStack[-1]:
                return False

            tagStack.pop()

        tagReport = getNextTagFromReport(tagReport)

    return len(tagStack) == 0


if __name__ == "__main__":
    brackets = ("(", ")", "{", "}", "[", "]")
    yeet = "(yeet){yeet}"
    yeeet = "({yeet})"
    yeeeet = "({yeet)}"
    yeeeeet = "(yeet"
    print(check_brackets(yeet, brackets))
    print(check_brackets(yeeet, brackets))
    print(check_brackets(yeeeet, brackets))
    print(check_brackets(yeeeeet, brackets))
    print()

    spam = "Hello, world!"
    eggs = "Hello, /* OOGAH BOOGAH world!"
    parrot = "Hello, OOGAH BOOGAH*/ world!"
    dead_parrot = "Hello, /*oh brave new */world!"
    print(remove_comments(spam, "/*", "*/"))
    print(remove_comments(eggs, "/*", "*/"))
    print(remove_comments(parrot, "/*", "*/"))
    print(remove_comments(dead_parrot, "/*", "*/"))
    print()

    otags = ("<head>", "<body>", "<h1>")
    ctags = ("</head>", "</body>", "</h1>")
    print(get_tag_prefix("<body><h1>Hello!</h1></body>", otags, ctags))
    print(get_tag_prefix("<h1>Hello!</h1></body>", otags, ctags))
    print(get_tag_prefix("Hello!</h1></body>", otags, ctags))
    print(get_tag_prefix("</h1></body>", otags, ctags))
    print(get_tag_prefix("</body>", otags, ctags))
    print()

    spam = (
        "<html>"
        "  <head>"
        "    <title>"
        "      <!-- Ici j'ai écrit qqch -->"
        "      Example"
        "    </title>"
        "  </head>"
        "  <body>"
        "    <h1>Hello, world</h1>"
        "    <!-- Les tags vides sont ignorés -->"
        "    <br>"
        "    <h1/>"
        "  </body>"
        "</html>"
    )
    eggs = (
        "<html>"
        "  <head>"
        "    <title>"
        "      <!-- Ici j'ai écrit qqch -->"
        "      Example"
        "    <!-- Il manque un end tag"
        "    </title>-->"
        "  </head>"
        "</html>"
    )
    parrot = (
        "<html>"
        "  <head>"
        "    <title>"
        "      Commentaire mal formé -->"
        "      Example"
        "    </title>"
        "  </head>"
        "</html>"
    )
    tags = ("html", "head", "title", "body", "h1")
    comment_tags = ("<!--", "-->")
    print(check_tags(spam, tags, comment_tags))
    print(check_tags(eggs, tags, comment_tags))
    print(check_tags(parrot, tags, comment_tags))
    print()
