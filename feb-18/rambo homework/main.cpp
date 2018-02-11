#include <iostream>
using namespace std;
int main()
{
    char mychar[] = { 'a','c','e',' ','o','f',' ','k','i','d','n','e','y','s'};
    int i = sizeof(mychar)-1;
    cout << mychar[i] << "b" << endl;
    return 0;
}
