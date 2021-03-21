var isajax = false
releasehold();
webservicehost='';
trackname ='t1';
servoname = 'gripper1'
var servovalues = {};
var trackvalues = {};
var jointvalues = [];
let ar3webservicehost = 'http://localhost:5000';
let ar3camserviceurl = 'http://localhost:8000/stream.mjpg';

maxmultiplier = 100
minmmultiplier = 1


    var gp ;
    var hasGP = false;
    var repGP;
    var labels = ['a:Press and Play Joystick for linear movement','b:get position string','x:servo open','y:servo close','l/--','r/++','l2/t1','r2/t1','back:override rest position','start:calibrate','left axis press/no use','right axis press/no use','up/j5','down/j5','left/j6','right/j6','xbox:rest position']
    var axislabels = ['left x/j1','left y/j2','right x/j4','right y/j3']
    var prevdata_buttons=[]
    var prevdata_axis = []

    function canGame() {
        return "getGamepads" in navigator;
    }

    function reportOnGamepad() {
        gp = navigator.getGamepads()[0];
        var html = "";
            html += "id: "+gp.id+"<br/>";

        for(var i=0;i<gp.buttons.length;i++) {
            html+= "Button "+(i+1)+" ("+labels[i]+"): ";
            if(gp.buttons[i].pressed)
            {
                html+= " pressed";
                addCommand(i,gp.buttons[i],'button');
            }
            html+= "<br/>";
        }

        for(var i=0;i<gp.axes.length; i++) {
           var data1 = parseInt(gp.axes[i]);
            html+= axislabels[i]+" Stick "+ ": "+data1+"<br/>";
            if(data1==1 || data1==-1 )
            {
                addCommand(i,data1,'axis');
            }
        }

        $("#gamepadDisplay").html(html);
    }

    $(document).ready(function() {

        if(localStorage.getItem('ar3webservicehost'))
        {
           ar3webservicehost= localStorage.getItem('ar3webservicehost')
        }
        if(localStorage.getItem('ar3camserviceurl'))
        {
           ar3camserviceurl= localStorage.getItem('ar3camserviceurl')
        }

        $('#webservicehost').val(ar3webservicehost)
        $('#webcamurl').val(ar3camserviceurl);
        releasehold()
        connectCamera();
        drawJslider();
        if(canGame()) {

            var prompt = "Use Joystic (Select and press any button in controller)";
            $("#gamepadPrompt").text(prompt);

            $(window).on("gamepadconnected", function() {
                hasGP = true;
                $("#gamepadPrompt").html("Gamepad connected!");
                console.log("connection event");
                repGP = window.setInterval(reportOnGamepad,20);
            });

            $(window).on("gamepaddisconnected", function() {
                console.log("disconnection event");
                $("#gamepadPrompt").text(prompt);
                window.clearInterval(repGP);
            });

            //setup an interval for Chrome
            var checkGP = window.setInterval(function() {
                console.log('checkGP');
                if(navigator.getGamepads()[0]) {
                    if(!hasGP) $(window).trigger("gamepadconnected");
                    window.clearInterval(checkGP);
                }
            }, 500);
        }


    });



    function drawJslider()
    {
        template = '<div class="col"><p>'+
                                      '<label class="form-label">@element_id</label>'+
                                      '<button class="btn btn-primary movejoint" data-element_id="@element_id" data-type="reduce">@min</button>'+
                                        '<input type="range" min="@min" max="@max" value="@default" class="slider" id="@element_id" step="0.01">'+
                                      '<button class="btn btn-primary movejoint" data-element_id="@element_id" data-type="increase">@max</button>'+
                                      ' <span id="text_@element_id"></span>'+
                                  '</p></div>';
        data = {
            J1: { min: -170, max: 170, default: 0, element_id:'J1'},
            J2: { min: -129.6, max: 0, default: -90, element_id:'J2'},
            J3: { min: 1, max: 143.7, default: 1.05, element_id:'J3'},
            J4: { min: -164.5, max: 164.5, default: 0, element_id:'J4'},
            J5: { min: -104.15, max: 104.15, default: 0, element_id:'J5'},
            J6: { min: -148.1, max: 148.1, default: 0, element_id:'J6'},
        };
        html='<h4>Move Joint</h4>';
        $.each(data,function(i,v){
            tmp = template;
            $.each(v,function(label,value){
                tmp=tmp.replace('@'+label,value).replace('@'+label,value).replace('@'+label,value).replace('@'+label,value).replace('@'+label,value);
            });
            html+=tmp;
        });

        $('#moveJointCtrlContainer').html(html);
        $(document).on('input','.slider',function()
        {
            let v = $(this).val()
            let el_id = $(this).attr('id');
            $('#text_'+el_id).html(v);

        });


        $(document).on('mouseup','.slider',function(){

            let element_id = $(this).attr('id');
            setJointValue(element_id,this.value);
        });
        $(document).on('keyup','.slider',function(){

            let element_id = $(this).attr('id');
            setJointValue(element_id,this.value);
        });

        $('.btn-movelinear').unbind().on('click',function(){
            let data={x:0,y:0,z:0};
            let axis = $(this).data('axis');
            console.log('click');
            let operator  = $(this).data('operator');
            let value = parseFloat($('#multiplyer').val());
            if(operator == '-')
            {
                    data[axis] -= value ;
            }
            else
            {
                    data[axis] += value ;
            }
            moveLinear(data);


        });

        $('.movejoint').unbind().on('click',function(){
            let multiplyer = parseFloat($('#multiplyer').val());
            let type = $(this).data('type');
            let element_id = $(this).data('element_id');
            let el = $('#'+element_id);
            if(type=='increase')
            {
                let newvalue = parseFloat(el.val()) + multiplyer;
                setJointValue(element_id,newvalue);
            }
            else if(type=='reduce')
            {
                let newvalue = parseFloat(el.val()) - multiplyer;
                setJointValue(element_id,newvalue);
            }
            else
            {

            }
        })

    }



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
    localStorage.setItem('ar3camserviceurl',webcamurl);
    $('#ar3cameraimage').attr('src',webcamurl);

}
function connectWebService()
{
    alert("connect web service, not yet ready");
}

function connectMachine()
{
    let ischecked = $('#usegamepad').prop('checked')
    if(ischecked)
    {
        fetchArmInfo();
    }

}

// use for move linear only. it separate from default movement to avoid confusion
function useLinearMovement(i)
{
    console.log('useLinearMovement',i)
    webservicehost = $('#webservicehost').val();
    url=webservicehost + '/move_l/';
    mm = parseInt($('#multiplyer').val());

    if(i==6) //
    {
        url+='y';
        mm = mm*-1;
    }
    else if(i==7) //
    {
        url+='y';
    }
    else if(i==12) //
    {
        url+='z';
    }
    else if(i==13) //
    {
        url+='z';
        mm = mm *-1;
    }
    else if(i==14) //
    {
        url+='x';
        mm = mm * -1;
    }
    else if(i==15) //
    {
        url+='x';
    }
    data = {mm:mm};
    jsonajax(url,data).done(function(r){
					releasehold();
					isajax=false;

					    if(r['code']=='OK')
					    {
					        fetchArmInfo();//   addCommand(0,1,'button');
					    }
					    else
					    {
					        $('#statuscode').val(r.code);
                            $('#statusmsg').val(r.msg);
					    }



				}).fail(function(e){
					console.error(e)
					releasehold();
					isajax=false
				})

}


function checkIsLinearMovement(i)
{
    var avalue = gp.buttons[0]['pressed'];

    if(avalue)
    {
        let dirbutton_index = [6,7,12,13,14,15];//l2,r2, up,down,left,right
        if(dirbutton_index.includes(i))
        {
            console.log('checkIsLinearMovement:true');
            return true;
        }
        else
        {
            console.log('checkIsLinearMovement:false');
            return false;
        }

    }
    else
    {
        console.log('checkIsLinearMovement:false');
        return false;
    }


}


function addCommand(i,value,type)
{
	//previous ajax not finish, not accept any command
    let isusegamepad = $('#usegamepad').prop('checked');

	if(!isajax && isusegamepad)
	{
	        $('#setpositionurl').val('');
	        islinearmovement =false;
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
				    if(checkIsLinearMovement(i)) //press a and hold, then go up/down/left/right shall run different linear routine
				    {
                        useLinearMovement(i);
                        return false;
				    }
					else if(i==12)//up
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

				    if(checkIsLinearMovement(i)) //press a and hold, then go up/down/left/right shall run different linear routine
				    {
				        useLinearMovement(i);
				        return false;
				    }


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
				else if(i==0) //it is modifier button for others button
				{
                    url='';
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




					if(getpositionstring)
					{
					    $('#setpositionurl').val(r['msg']);
					    $('#setpositionurl').select();
					}
					else  //there is movement, will force download latest info
					{

					    if(r['code']=='OK')
					    {
					        fetchArmInfo();//   addCommand(0,1,'button');
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


function fetchArmInfo()
{
    webservicehost = $('#webservicehost').val();
	url=webservicehost+'/info'

    localStorage.setItem("ar3webservicehost", webservicehost);


    jsonajax(url,'').done(function(r)
    {
        jointvalues = r['jointvalues'];
        displayArmInformation(r);
        $('.arm_operationbody').show();
    }).fail(function(e)
    {
            alert("Server is unreachable.");
            $('.arm_operationbody').hide();
    })
}

function setJointValue(jointno,v)
{
    $('#'+jointno).val(v)
    $('#text_'+jointno).html($('#'+jointno).val());
    let url =$('#webservicehost').val();
    url += '/move_j/'+jointno
    data = { movetype:'absolute', degree: v };
    console.log(url);

    jsonajax(url,data).done(function(r)
    {
        jointvalues = r['jointvalues'];
        displayArmInformation(r);
        $('.arm_operationbody').show();
    }).fail(function(e)
    {
//            alert("Server is unreachable.");
//            $('.arm_operationbody').hide();
    })
}

function moveLinear(data)
{
    console.log('moveLinear');
    let myurl = ar3webservicehost + '/move_l';
    jsonajax(myurl,data).done(function(r)
    {
        console.log(r)
    }).fail(function(e)
    {
        console.log(e)
        //            alert("Server is unreachable.");
        //            $('.arm_operationbody').hide();
    })
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
            $('#J'+indexvalue).val(v['degree']);
            $('#text_J'+indexvalue).html(v['degree']);
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
        $('#statuscode').val('');
        $('#statusmsg').val('');
    }
    catch(e){
        consoloe.err(e)
    }

}