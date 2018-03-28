#include <iostream>
#include <opencv2\opencv.hpp>

using namespace std;
using namespace cv;

Mat res;

//¾Ö²¿huMoment
int main()
{
	int neighbor_r=5;
	int bianchang = 2*neighbor_r+1;
	int huBins=7;
	Mat img = imread("nrrd2.png",0);

	Mat img_pad;
	copyMakeBorder(img,img_pad,neighbor_r,neighbor_r,neighbor_r,neighbor_r,BORDER_REPLICATE);

	const int size_res_map[3]={img.rows,img.cols,huBins};
	Mat resMap(3,size_res_map,CV_32FC1);

	for(int y=neighbor_r;y<img_pad.rows-neighbor_r;y++)
		for(int x=neighbor_r;x<img_pad.cols-neighbor_r;x++)
		{
			Mat roi = img_pad(Rect(x-neighbor_r,y-neighbor_r,bianchang,bianchang));

			Moments mom;
			mom = moments(roi);
			double hu[7];
			HuMoments(mom,hu);

			for(int i=0;i<huBins;i++)
				resMap.at<float>(y-neighbor_r,x-neighbor_r,i) = float(hu[i]);

		}


	res=resMap;
	cout<<res.at<float>(100,100,3);
	imshow("qq",img);
	waitKey(0);
	return 0;
}