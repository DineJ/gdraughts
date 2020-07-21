from distutils.core import setup, Extension
from distutils.command.clean import clean
from glob import glob
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

def create_localised_files():
    mo_files = []
    # os.system('bash create_po.sh')
    os.system('make -C po')
    os.system('make -C po DESTDIR=../ install')
    mo_files.append(('share/locale/de/LC_MESSAGES/', ['locale/de/LC_MESSAGES/gdraughts.mo']))
    mo_files.append(('share/locale/en/LC_MESSAGES/', ['locale/en/LC_MESSAGES/gdraughts.mo']))
    mo_files.append(('share/locale/es/LC_MESSAGES/', ['locale/es/LC_MESSAGES/gdraughts.mo']))
    mo_files.append(('share/locale/fr/LC_MESSAGES/', ['locale/fr/LC_MESSAGES/gdraughts.mo']))
    mo_files.append(('share/locale/it/LC_MESSAGES/', ['locale/it/LC_MESSAGES/gdraughts.mo']))
    mo_files.append(('share/locale/nl/LC_MESSAGES/', ['locale/nl/LC_MESSAGES/gdraughts.mo']))
    mo_files.append(('share/applications',['desktop/gdraughts.desktop']))
    return mo_files

class CleanFiles(clean):
    def run(self):
        super().run()
        cmd_list = dict(
            po_clean='make -C po clean',
            irm_locale_and_desktop='rm -rf locale gdraughts.desktop'
        )
        for key, cmd in cmd_list.items():
            os.system(cmd)


setup (name = 'gdraughts',
    version = '0.1',
    description = 'A Draughts Program',
    author='Dine Jridi',
    author_email='dinejridi@gmail.com',  
    url='https://gitlab.com/DINE_J/international-checkers-game', 
    long_description=read("Readme"),
    platforms = ['Linux'],

    license = "GPLv3+",

    packages=['gdraughts'],

    cmdclass={
        'clean': CleanFiles,
    },

    classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: X11 Applications :: GTK',
          'Intended Audience :: End Users/Desktop',                
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: POSIX :: Linux',          
          'Programming Language :: Python :: 3',
          'Topic :: Games/Entertainment :: Board Games',
          ],
    data_files = [("share/gdraughts/images", glob('images/*.jpg')),
            ("share/doc/gdraughts-0.1", ["Readme", "LICENSE", "gdraughts/it-help.txt", "gdraughts/fr-help.txt", "gdraughts/en-help.txt", "gdraughts/nl-help.txt", "gdraughts/sp-help.txt"]),
            ('share/pixmaps', ['gdraughts.png']),
    ]+ create_localised_files()

               
    )
