from hypothesis.strategies import from_regex

username_strategy = from_regex(r"\A[a-z_][a-z0-9_]{0,30}\Z")

password_strategy = from_regex(r"\A[\w\d\,\.\!\@\#\$\%\^\&\*\(\)\-\_\=\+\[\]\{\}\\\|\`\~\/\?\'\"\;\:]{1,}\Z")
