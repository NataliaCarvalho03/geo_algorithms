/*


By downloading, copying, installing or using the software you agree to this license. If you do not agree to this license, do not download, install, copy or use the software.

License Agreement
For Open Source Computer Vision Library
(3-clause BSD License)

Copyright (C) 2000-2018, Intel Corporation, all rights reserved.
Copyright (C) 2009-2011, Willow Garage Inc., all rights reserved.
Copyright (C) 2009-2016, NVIDIA Corporation, all rights reserved.
Copyright (C) 2010-2013, Advanced Micro Devices, Inc., all rights reserved.
Copyright (C) 2015-2016, OpenCV Foundation, all rights reserved.
Copyright (C) 2015-2016, Itseez Inc., all rights reserved.
Third party copyrights are property of their respective owners.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
Neither the names of the copyright holders nor the names of the contributors may be used to endorse or promote products derived from this software without specific prior written permission.

This software is provided by the copyright holders and contributors "as is" and any express or implied warranties, including, but not limited to, the implied warranties of merchantability and fitness for a particular purpose are disclaimed. In no event shall copyright holders or contributors be liable for any direct, indirect, incidental, special, exemplary, or consequential damages (including, but not limited to, procurement of substitute goods or services; loss of use, data, or profits; or business interruption) however caused and on any theory of liability, whether in contract, strict liability, or tort (including negligence or otherwise) arising in any way out of the use of this software, even if advised of the possibility of such damage.


*/

#include <iostream>
#include <sstream>
#include <string>
#include <ctime>
#include <cstdio>

#include <opencv2/core.hpp>
#include <opencv2/core/utility.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/calib3d.hpp>
#include <opencv2/calib3d/calib3d_c.h>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>
//#include"stdafx.h"
#include<fstream>

using namespace std;
using namespace cv;


Size patternSize = Size(7,9); //Declarando o tamanho do tabuleiro em pontos
vector<vector<Point2f>> corners; //Vetor de vetores, cada vetor interno tem as coordenadas dos pontos detectados em cada imagem
vector<vector<Point3f>> final_corners;
Size zero_zone = Size(-1, -1);
TermCriteria criteria = TermCriteria(CV_TERMCRIT_EPS + CV_TERMCRIT_ITER, 40, 0.001); 
Mat cameraMatrix;
Mat distCoeffs;
vector<Mat> rvecs;
vector<Mat> tvecs;

int main(){

    cout<<"==========================================================================="<<endl;
    cout<<"Algoritmo para Calibração de câmeras utilizando a biblioteca OpenCV"<<endl;
    cout<<"Desenvolvido por Natália C. Amorim - Universidade Federal do Paraná (UFPR)"<<endl;
    cout<<"Orientador: Prof. Edson A. Mitishita"<<endl;
    cout<<"==========================================================================="<<endl;

    
    // --------------- Lendo as imagens do Tabuleiro ---------------------------
    vector<cv::String> fn;
    glob("tabuleiro2/*.JPG", fn, false); //get a list of file names

    vector<Mat> images; //Vector of matrix
    size_t count = fn.size(); //number of png files in images folder

    for (size_t i=0; i<count; i++){
        Mat grayImage = imread(fn[i]);
        grayImage.convertTo(grayImage, CV_8U, 1 / 256.0);
        
        images.push_back(grayImage); //Read each file of the file list and store it on "images"
    }
    //cout<<"estou aqui!"<<endl;
    //----------------- Detectando os pontos no tabuleiro -----------------------
    int vec_aux[images.size()];

    for(int i=0 ; i<images.size() ; i++){

        vector<Point2f> temp;
        vec_aux[i] = findChessboardCorners(images[i], patternSize, temp);  
        cout<<vec_aux[i]<<endl;      
        corners.push_back(temp);
    }
    
    
    //---------------- Refinando as coordenadas -----------------------------------

    //for (int i=0 ; i < images.size(); i++){
      //  cornerSubPix(images[i] , corners[i], patternSize, zero_zone, criteria);
    //}

    // Convertendo para a forma homogenea ----------------------------------------
    for (int i =0 ; i<corners.size() ; i++){
        vector<Point3f> temp_homog_corner;
        convertPointsToHomogeneous(corners[i], temp_homog_corner);
        final_corners.push_back(temp_homog_corner);
    }
    //cout<<"Estou aqui!"<<endl;


    // -------- Preparando as coordenadas do tabuleiro para a calibração ---------
    // ----------------------- Coorndenadas em cm --------------------------------
    string fileName = "default.xml";
    FileStorage fs(fileName, FileStorage::READ);
    fs.open(fileName, FileStorage::READ);

    vector<vector<Point3f>> objPoints;
    //cout<<final_corners[1]<<endl;
    for (int i=0 ; i<final_corners.size(); i++){   
        vector<Point3f> temp_aux;
        fs["chessboard_coord"]>>temp_aux;
        //cout<<temp_aux<<endl;
        objPoints.push_back(temp_aux);
    }    
    //cout<<objPoints[1].size()<<endl;
    //cout<<objPoints.size()<<", "<<corners.size()<<endl<<objPoints[1].size()<<", "<<corners[1].size()<<endl;

    fs.release();

    // ---------------- Calibrando -----------------------------------------------

    double rms = calibrateCamera(objPoints, corners, images[0].size(), cameraMatrix, distCoeffs, rvecs, tvecs, 0, criteria); 
    double aperture_diameterx = 8.6,aperture_diametery = 6.6 , fovx, fovy, focal_lenght, aspect_ratio; //milimeters
    Point2d principalPoint;

    // ----------------- Obtendo valores de f em milímetros ----------------------
    calibrationMatrixValues(cameraMatrix, images[0].size(), aperture_diameterx, aperture_diametery, fovx, fovy, focal_lenght, principalPoint, aspect_ratio);

    //cout<<cameraMatrix<<endl;

    //cout<<rms<<endl;

    //cout<<focal_lenght<<endl;

    //------------ Saída no monitor -----------------------------------------------
    cout<<"========================= Resultado Final ================================="<<endl;
    cout<<"Matriz da câmera: "<<endl;
    cout<<cameraMatrix<<endl;
    cout<<"==========================================================================="<<endl;
    cout<<"Distância focal (mm): "<<focal_lenght<<endl;
    cout<<"Coordenadas do PP (pixel): "<<cameraMatrix.at<double>(0,2)<<", "<<cameraMatrix.at<double>(1,2)<<endl;
    cout<<"==========================================================================="<<endl;
    cout<<"Coeficientes de distorção: "<<endl;
    cout<<"k1: "<<distCoeffs.at<double>(0,0)<<"\t"<<"k2: "<<distCoeffs.at<double>(0,1)<<"\t"<<"k3: "<<distCoeffs.at<double>(0,4)<<endl;
    cout<<"p1: "<<distCoeffs.at<double>(0,2)<<"\t"<<"p2: "<<distCoeffs.at<double>(0,3)<<endl;
    cout<<"fovx: "<< fovx<<endl;
    //cout<<cameraMatrix.type()<<endl;
}
