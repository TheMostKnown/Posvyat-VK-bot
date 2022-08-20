import re


def make_domain(link: str) -> str:
    domain = re.sub(r'[@*]?|(.*vk.com/)', '', link.lower())

    return domain
