/*function KeyPress(evt) 
{
    evt = evt || window.event;
    var charCode = evt.keyCode || evt.which;
    var charStr = String.fromCharCode(charCode);
    alert(charStr);
};

*/



/*BULLSHIT*/
var ee = false;
var inside = true;
var insiderange = 20;
var enablemouse=0;

ballsize=23;

var mousex = 0;
var mousey = 0;

function handler(e) {
    e = e || window.event;

    var pageX = e.pageX;
    var pageY = e.pageY;

    if (pageX === undefined) {
        pageX = e.clientX + document.body.scrollLeft + document.documentElement.scrollLeft;
        pageY = e.clientY + document.body.scrollTop + document.documentElement.scrollTop;
    }
    mousex = pageX;
    mousey = pageY;
}


var Key = 
{
    _pressed: {},
  
    LEFT: 37,
    UP: 38,
    RIGHT: 39,
    DOWN: 40,
    SHIFT: 16,

    isDown: function(keyCode) {
      return this._pressed[keyCode];
    },
    
    onKeydown: function(e) {
      code = (e.keyCode)? e.keyCode: e.which;
      if(code==27)
      {
          if(ee==false)ee=true;
          else
          {
              enablemouse+=1;
              if(enablemouse>2)enablemouse=0;
          }
      }
      this._pressed[code] = true;
    },
    
    onKeyup: function(e) {
      code = (e.keyCode)? e.keyCode: e.charCode;
      delete this._pressed[code];
    }
};

var multiplier = 1.5;

var startposx = 33;
var startposy = 46;
var startvx = 4;
var startvy = -4;

var posx = startposx;
var posy = startposy;

var vx = startvx;
var vy = startvy;

var accel = 0.6;

var grav = -0.4;

var wallleft=0;
var walldown=0;
var wallup=500;
var wallright=500;

var maxv = 30;
var friction = 0.7;

function update()
{
    if(ee)
    {
        wallup = window.innerHeight-ballsize;
        wallright = window.innerWidth-ballsize;
    
        var oldx = posx;
        var oldy = posy;
    
        posx+=vx*multiplier
        if(posx<wallleft || posx>wallright)
        {
            posx = oldx;
            vx = -vx*friction;
        }
    
        posy+=vy*multiplier
        if(posy<walldown || posy>wallup)
        {
            posy = oldy;
            vy = -vy*friction;
        }
    
        if(posx<wallleft)posx=wallleft;
        if(posx>wallright)posx=wallright;
    
        if(posy<walldown)posy=walldown;
        if(posy>wallup)posy=wallup;
    
        if (Key.isDown(Key.UP))vy-=accel*multiplier;
        if (Key.isDown(Key.DOWN))vy+=accel*multiplier;
        if (Key.isDown(Key.LEFT))vx-=accel*multiplier;
        if (Key.isDown(Key.RIGHT))vx+=accel*multiplier;

        if (enablemouse != 1)vy-=grav/1.5*multiplier;
        
        mousedistx = posx+ballsize/2-mousex;
        mousedisty = posy+ballsize/2-mousey;

        sensx =  mousedistx>0? 1: -1;
        sensy =  mousedisty>0? 1: -1;

        mousedistx = Math.abs(mousedistx);
        mousedisty = Math.abs(mousedisty);

        totaldist = Math.sqrt(mousedistx**2+mousedisty**2);
        influx = mousedistx/(mousedistx+mousedisty)
        influy = mousedisty/(mousedistx+mousedisty)


        if (enablemouse == 1)
        {
            vx-=sensx*0.005*influx*totaldist;
            vy-=sensy*0.005*influy*totaldist;
            vx*=0.9;
            vy*=0.9;
        }
        if(enablemouse == 2)
        {
            vx+=sensx*100*influx/totaldist;
            vy+=sensy*100*influy/totaldist;
            vx*=0.98;
            vy*=0.98;
        }
        if(enablemouse == 0)
        {
            vx*=0.999;
            vy*=0.999;
        }
        if(vx>maxv)vx = maxv;
        if(vx<-maxv)vx=-maxv;
        if(vy>maxv)vy = maxv;
        if(vy<-maxv)vy=-maxv;

        
        var near = Math.abs(posx-startposx)<insiderange && Math.abs(posy-startposy)<insiderange;
        if(!inside && near)
        {
            inside = true;
            posx = startposx;
            posy = startposy;
            vx = startvx;
            vy = startvy;
            ee=false;
            enablemouse=0;
        }
        else if(!near)inside = false; 
        
        document.getElementById("ball").style.left=posx + "px";
        document.getElementById("ball").style.top=posy + "px";
    }  
}
/*FIN BULLSHIT*/