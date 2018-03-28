#include <iostream>
#include <opencv2\opencv.hpp>

using namespace std;
using namespace cv;

Mat res;

//局部hog
int main()
{
	int neighbor_r=5;
	int hogBins=9;
	float step_ori=2*CV_PI/hogBins;
	Mat img = imread("nrrd2.png",0);

	Mat img_pad;
	copyMakeBorder(img,img_pad,neighbor_r,neighbor_r,neighbor_r,neighbor_r,BORDER_REPLICATE);

	const int size_res_map[3]={img.rows,img.cols,hogBins};
	const int size_hog_map[3]={img_pad.rows,img_pad.cols,2};

	Mat resMap(3,size_res_map,CV_32FC1);
	Mat hogMap(3,size_hog_map,CV_32FC1);


	Mat img_pad2;
	copyMakeBorder(img_pad,img_pad2,1,1,1,1,BORDER_REPLICATE);
	for(int y=1;y<img_pad2.rows-1;y++)
		for(int x=1;x<img_pad2.cols-1;x++)
		{
			double dx = img_pad2.at<uchar>(y,x+1)-img_pad2.at<uchar>(y,x-1);
			double dy = img_pad2.at<uchar>(y+1,x)-img_pad2.at<uchar>(y-1,x);
			
			hogMap.at<float>(y-1,x-1,0)=sqrt(dx*dx + dy*dy);
			
			//atan2返回[-Pi, Pi]的弧度值
			float oriTemp =  atan2(dy, dx);
			if(oriTemp<0)
				oriTemp += 2*CV_PI;//转换成0~2PI
			hogMap.at<float>(y-1,x-1,1)=oriTemp;
		}


	for(int y=neighbor_r;y<img_pad.rows-neighbor_r;y++)
		for(int x=neighbor_r;x<img_pad.cols-neighbor_r;x++)
		{
			for(int j=y-neighbor_r;j<=y+neighbor_r;j++)
				for(int i=x-neighbor_r;i<=x+neighbor_r;i++)
				{

				    //统计梯度直方图 
			        for(int k=0;k<hogBins;k++)
				        if((hogMap.at<float>(j,i,1) >= (k*step_ori)) && (hogMap.at<float>(j,i,1) < ((k+1)*step_ori)) )
						{resMap.at<float>(y-neighbor_r,x-neighbor_r,k) += hogMap.at<float>(j,i,0); break;} 
				}
		}

		res=resMap;
		cout<<res.at<float>(10,10,0);
	imshow("qq",img);
	waitKey(0);
	return 0;
}