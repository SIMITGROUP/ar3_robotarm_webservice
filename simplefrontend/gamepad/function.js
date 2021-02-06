var isajax = false
releasehold();
webservicehost='';
trackname ='t1';
servoname = 'gripper1'
maxmultiplier = 100
minmmultiplier = 1
function jsonajax(url,data,method='get'){

	return $.ajax({
		url : url,
		data : data,
		dataType: 'json',
		method : method
	});
}

function simpleajax(url,data,method='get'){

	return $.ajax({
		url : url,
		data : data,		
		method : method
	});
}


function holdscreen()
{
	$('.holdinicator').show()	
}

function releasehold()
{

	$('.holdinicator').hide();
}
function addCommand(i,value,type)
{
	//previous ajax not finish, not accept any command
	if(!isajax)
	{
			multiplyer = parseInt($('#multiplyer').val())
			webservicehost = $('#webservicehost').val();
			url=webservicehost	
			isajax = true
			data={};
			$('.holdinicator').show();
			data=[];
			degree = 0 
			if(type == 'axis' || (type=='button' && i >=12 && i <=15) ) //2 joystick + up/down/left/right to control 6 axis
			{
				let jointname ='';

				if(type == 'axis')
				{
					if(i==0 || i==1)				
						jointname ='j'+(i+1);  //0=j1,1=j2	
					else if(i==2)
						jointname ='j4'
					else if(i==3)
						jointname ='j3'					

					degree = value * multiplyer;	
				}
				else //button
				{
					if(i==12)//up
					{
						jointname ='j5';
						degree = multiplyer * -1;
					}
					else if(i==13)//down
					{
						jointname ='j5';
						degree = multiplyer ;
					}
					else if(i==14)//left
					{
						jointname ='j6';
						degree = multiplyer ;
					}
					else //right
					{
						jointname ='j6';
						degree = multiplyer * -1;
					}

				}
				
				url += '/move_j/'+jointname
				data = {
					movetype:'move',
					degree: degree
				}
			}
			else if (type == 'button')
			{
				if(i >=6 && i <=7)
				{
					mm=0;
					if(i==6)
					{
						mm=multiplyer* -1
					}
					else
					{
						mm=multiplyer*1
					}
					url += '/movetrack/'+trackname
					data = {
						movetype:'move',
						mm: mm
					}
				}
				else if (i >=10 && i <=11)
				{
					myvalue=""
					if(i==10)
					{
						myvalue="close"
					}
					else
					{
						myvalue="open"	
					}
					url += '/servo/'+servoname
					data = {						
						value: myvalue
					}
				}
				else if(i >=4 && i <=5)
				{
					if(i==4)
					{
						multiplyer = multiplyer - 1	
					}
					else
					{
						multiplyer = multiplyer + 1	
					}

					if( multiplyer < minmmultiplier)
					{
						multiplyer=minmmultiplier
					}
					else if(multiplyer > maxmultiplier)
					{
						multiplyer=maxmultiplier //control maximum 200
					}

					url=''
					$('#multiplyer').val(multiplyer);
				}
				

			}



			if(url!='')
			{
				jsonajax(url,data).done(function(r){
					console.log(r)
					releasehold();
					isajax=false
					
				}).fail(function(e){
					console.error(e)
					releasehold();
					isajax=false
				})
			}
			else
			{
					releasehold();
					isajax=false

			}
			

	}
	

}