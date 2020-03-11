#include "photo.h"
#include <iostream>
//#include "tiePoint.h"

int main(){

    std::cout << "Hello hell" << std::endl;

    photo myPhotos;

    std::vector< std::vector<std::string> > myPhotosData = myPhotos.loadPointsAndPhotos();
    std::vector<photo> separatedPhotos = myPhotos.separatePhotos(myPhotosData);

    std::vector<std::string> photosToBeConverted = photo::definePhotosToBeConverted();

    for (int i = 0; i < separatedPhotos.size(); i++){
        separatedPhotos.at(i).convertToPx();
    }

    std::vector<tiePoint> tiePoints;

    if (photosToBeConverted.at(0) == "all"){
        std::cout << "Vou escrever todas as fotos!" << std::endl;
        tiePoints = photo::organizePoints(separatedPhotos);
        photo::writeTiePoints(tiePoints, separatedPhotos);
    }else{
        photo::convertToLPS(photosToBeConverted, separatedPhotos);
    }


    //for (int i = 0; i < separatedPhotos.size(); i++){
        //separatedPhotos.at(i).convertToLPS();
    //}


    return 0;
}
