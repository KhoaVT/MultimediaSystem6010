#include <iostream>
#include <conio.h>
#include <fstream>
#include <string>
#include <vector>


using namespace std;
//

int rowA =0;
int colA =0;

int x=4; //the size of the image
int y=4; //the size of the image

int *ArrayT =new int[x*y]; //an array to store the pixel value when the program read that file
vector<int> Temp; //vector to content the values of pixel after eliminating the pixels that has more than two times
vector<int> countPixel;
int main()
{
    cout << "***************************************************" << endl;
    cout << "Homework, retrieving image and clip:" << endl;
    cout << "***************************************************" << endl;
    ifstream ReadImage("Image.txt");
	int pixel;
	string linaA;
	if (ReadImage.is_open()){
	    while (ReadImage >>pixel){
                ArrayT[colA]=pixel;
                colA++;
        }
            ReadImage.close();

	}
    else {
           cout <<"file is not open";
    }

    cout << "Read the value of the pixel and store in an array:" << endl;
     for (int i=0; i<(x*y); i++){
       cout << ArrayT[i] <<" ";
    }
    cout <<'\n';

  cout << "The pixels after being eliminated those appear more than twice:" << endl;
    Temp.push_back(ArrayT[0]);
    bool findt = true;
    for (int i= 0; i<(x*y); i++){
        findt= true;
        for (int j=0; j<(x*y); j++){
            if (Temp[j] == ArrayT[i]){
                findt = false;
                break;
            }
        }
        if (findt==true){
            Temp.push_back(ArrayT[i]) ;

        }

    }
    cout <<'\n';
    for (int i=0; i<Temp.size(); i++){
        cout <<Temp[i]<< " ";
    }
//starting the count pixel
cout <<'\n';
    for (int i=0; i<Temp.size(); i++){
            int k=0;
        for (int j=0; j<(x*y); j++){
            if (Temp[i]==ArrayT[j]){
                k++;
            }
        }
        countPixel.push_back(k);
    }
//Printing out the count pixel
cout <<"The count pixel accordingly: "<< endl;
for (int i=0; i<countPixel.size();i++)
    cout <<countPixel[i]<< " ";

	getch();
    return 0;
}
