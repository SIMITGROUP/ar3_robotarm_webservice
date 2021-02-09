var isajax = false
releasehold();
webservicehost='';
trackname ='t1';
servoname = 'gripper1'
var servovalues = {};
var trackvalues = {};
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

function connectCamera()
{
    let webcamurl = $('#webcamurl').val();
    $('#ar3cameraimage').attr('src',webcamurl);

}

function connectMachine()
{
    let ischecked = $('#usegamepad').prop('checked')
    if(ischecked)
    {
        addCommand(0,1,'button');
    }

}

function addCommand(i,value,type)
{
	//previous ajax not finish, not accept any command
    let isusegamepad = $('#usegamepad').prop('checked');

	if(!isajax && isusegamepad)
	{
	        $('#setpositionurl').val('');
	        getpositionstring = false;
			multiplyer = parseInt($('#multiplyer').val())
			webservicehost = $('#webservicehost').val();
			url=webservicehost	
			isajax = true
			data={};
			$('.holdinicator').show();
			data=[];
			degree = 0;
			showinfo=false;
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
				else if (i >=2 && i <=3)
				{
					myvalue=0
					lastdegree = servovalues[servoname];

					if(i==2)
					{
						myvalue= lastdegree - multiplyer;
					}
					else
					{
						myvalue= lastdegree + multiplyer;
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
				else if(i==1)
				{
				    url+='/getposition';
				    getpositionstring=true;
				}
				else if(i==8)
				{
				    url += '/calibrate/setrest';
				}
				else if(i==9)
				{
				    url += '/calibrate/all';
				}
				else if(i==0)
				{
				    url += '/info';
				    showinfo=true;
				}
				else if(i==16)
				{
                    url += '/movetorestposition';
				}
				else
				{
				    url='';
				}
				

			}



			if(url!='')
			{
				jsonajax(url,data).done(function(r){

					releasehold();
					isajax=false;

					if(showinfo) //if show info, just draw and finish
					{
					    displayArmInformation(r);
					}
					if(getpositionstring)
					{
					    $('#setpositionurl').val(r['msg']);
					    $('#setpositionurl').select();
					}
					else  //there is movement, will force download latest info
					{

					    if(r['code']=='OK')
					    {
					        addCommand(0,1,'button');
					    }
					    else
					    {
					        $('#statuscode').val(r.code);
                            $('#statusmsg').val(r.msg);
					    }

					}
					
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


function displayArmInformation(data)
{
    try{

        var board = data['board'];
        var jointvalues = data['jointvalues'];
        servovalues = data['servovalues'];
        trackvalues = data['trackvalues'];
        var txt = '';

        jointtxt='';
        $.each(jointvalues,function(index,v){
            indexvalue = parseInt(index)+1;

            jointtxt+='    J'+ indexvalue + ': '+v['degree']+' ('+v['step']+")\n"
        });

        servotxt='';
        $.each(servovalues,function(index,v){
            servotxt+='    '+ index + ': '+v+"\n"
//            servovalues[index]=v;

        });

        tracktxt='';
        $.each(trackvalues,function(index,v){
            tracktxt+='    '+ index + ': '+v['mm']+' ('+v['step']+")\n"
        });

        txt="Board: "+board+"\n"+
            "Joints:\n"+ jointtxt +"\n"+
            "Servo:\n"+ servotxt +"\n"+
            "Travel Track:\n"+ tracktxt +"\n";
        $('#txtArmInfo').val(txt);
    }
    catch(e){
        consoloe.err(e)
    }

}