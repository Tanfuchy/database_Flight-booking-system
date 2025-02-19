#include<cstdio>
#include<iostream>
#include<cstdlib>
#include<ctime>
using namespace std;

const char* location[7] = {"大连","芜湖","北京","上海","武汉","深圳","西安"};
string locate[7]= {"大连","芜湖","北京","上海","武汉","深圳","西安"};
string qu[]={"甘井子区","中山区","海淀区","大兴区","市中心"}; 
string tt;
int main()
{
	srand(time(NULL));
	int total_num=42;
	int price,seats,i,j,k=1;
	
	FILE *f = fopen("3_insert_flight.sql.sql", "w");
    fprintf(f, "insert into FLIGHTS values");
	for(i=0;i<7;i++){
		for(j=0;j<7;j++){
			if(i==j) continue;
				price=250+rand()%21*60;
				seats =50+rand()%6*5;
				fprintf(f, "('1%04d', %d, %d, %d, \"%s\", \"%s\")%c\n", k++, price, seats, seats,location[i],location[j], k==total_num?';':',');
		}
	}
	fclose(f);

	FILE *f1 = fopen("3_insert_hotel.sql", "w");
	fprintf(f1, "insert into HOTELS values");
	int hotel_num;
	k=1;
	for(i=0;i<7;i++){
		for(j=0;j<5;j++){
			hotel_num=1+rand()%2;
			for(int m=0;m<hotel_num;m++){
				tt=locate[i]+qu[j];
				price=200+rand()%300;
				seats=50+rand()%10*5;
				fprintf(f1, "('1%02d', \"%s\", %d, %d, %d)%c\n", k++ , tt.c_str(), price, seats, seats, (i==6&&j==4&&m==hotel_num-1)?';':',');
			}
		}
		
	}
	fclose(f1);


	FILE *f2 = fopen("3_insert_bus.sql", "w");
	fprintf(f2, "insert into BUS values");
	k=1;
	for(i=0;i<7;i++){
		for(j=0;j<5;j++){
			tt=locate[i]+qu[j];
			price=50+rand()%10*5;
			seats=24+rand()%4*6;
			fprintf(f2, "('1%03d', \"%s\", %d, %d, %d)%c\n",k++, tt.c_str(), price, seats, seats, (i==6&&j==4)?';':',');
		}
	} 
	fclose(f2);
	return 0;
}
