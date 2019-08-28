using namespace std;
int main(){
	FILE *fin,*fout;
	maxDiff = 0;
	fin = fopen("axis.in","br");
	fout = fopen("axis.out","bw");
	int n,x0,y0,x1,y1,diff;
	float nList[n];
	fscanf(fin,"%d", &n);
	for(int i=0; i<n; i++){
		fscanf(fin,"%f",&nList[i]);
	}
	for(int i=0; i<n; i++){
		for(int j=i,j<n,j++){
			diff = nList[j] - nList[i];
			if(diff<0){
				diff = 0-diff;
			}
			if(diff>maxDiff){
				maxDiff = diff;
			}
		}
	}
	fprintf(fout,"%f")
	return 0;
}