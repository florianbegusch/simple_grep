# This is an example PKGBUILD file. Use this as a start to creating your own,
# and remove these comments. For more information, see 'man PKGBUILD'.
# NOTE: Please fill out the license field for your package! If it is unknown,
# then please put 'unknown'.

# See http://wiki.archlinux.org/index.php/Python_Package_Guidelines for more
# information on Python packaging.

# Maintainer: Your Name <youremail@domain.com>
pkgname=simple_grep
pkgver=1
pkgrel=11
pkgdesc=""
arch=('i686' 'x86_64')
url=""
license=()
groups=()
depends=('python' 'python-setuptools')
makedepends=()
provides=('simple_grep')
conflicts=()
replaces=()
backup=()
options=(!emptydirs)
install=
source=('git+ssh://git@github.com/florianbegusch/simple_grep.git')

# Temporary
md5sums=('SKIP')

build() {
	rm -rf $pkgname-$pkgver	
	mv $pkgname $pkgname-$pkgver

	rm -rf $pkgname
}

package() {
  cd "$srcdir/$pkgname-$pkgver"
  python setup.py install --root="$pkgdir/" --optimize=1
}

