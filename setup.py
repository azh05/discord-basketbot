from setuptools import setup, find_packages

setup(
    name='basketbot',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pandas', 'discord', 'requests', 'numpy', 'matplotlib', 'scikit-learn', 'beautifulsoup4'
    ],
    entry_points={
    'console_scripts': [
        'basketbot = bot.main:main',
    ],
    },
    package_data={
        'bot.historicaldata': ['historical_player_data.xlsx'],
    },
)