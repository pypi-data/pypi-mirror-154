import setuptools

setuptools.setup(
    name="BotCore",
    version="1.0.0",
    author="Maks Vinnytskyi",
    author_email="ownerofforest@gmail.com",
    description="Base core for telegram bots.",
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Tullp/botcore",
    license="MIT",
    packages=["BotCore"],
    install_requires=["pyTelegramBotApi"],
)
