#include <iostream>
#include <bits/stdc++.h>

using namespace std;

class test {
public:
    string teetname;

    string printname(bool format = false, string formattext = NULL) {
        if (format == true) {
            std::cout << formattext << teetname << std::endl;
            return teetname;
        }
        std::cout << "Teetname is " << teetname << std::endl;
        return teetname;
    }
};

int main() {
    test integeri;
    integeri.teetname = "tet";
    integeri.printname(true, "Yourname is ");
}
