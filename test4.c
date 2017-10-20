//gcc test2.c -lm -o test2 `pkg-config --cflags --libs gtk+-3.0` `pkg-config --cflags --libs glib-2.0`

#include <cairo.h>
#include <gtk/gtk.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdbool.h>
#include <math.h>
#include <time.h>
#include <string.h>
#include <sys/time.h>
#include <signal.h>

///////STRUCS///////////

typedef struct Ball Ball;

struct Ball
{
  float x;
  float y;
  float vx;
  float vy;
  float radius ;
  float r;
  float g;
  float b;
  GArray *attached;
  bool grouped;
};

/////////FUNCTIONS DECLARATIONS////////////

static gboolean onmouse(GtkWidget *widget, GdkEventMotion *event, gpointer user_data);
static gboolean onpress(GtkWidget *widget, GdkEventButton *event, gpointer user_data);
static gboolean onrelease(GtkWidget *widget, GdkEventButton *event, gpointer user_data);
static float randoma();
static float mimax(float x, int minx, int maxx,float r);
static bool inball(float x,float y, Ball* b);
static bool squarecol(float x,float y, float minx, float miny, float maxx, float maxy);
static bool ball_collisions(Ball* b, int minx, int miny, int maxx, int maxy);
static void ball_walls(Ball* b, int minx, int miny, int maxx, int maxy);
static void do_drawing(GtkWidget *widget,cairo_t *cr);
static void addball(float x,float y);
static int getBallIndex(GArray *arr,Ball * b);
static void ball_repulsion(Ball* b1, Ball* b2);
static void ball_attraction(Ball* b1, Ball* b2);
  


/////////VARIABLES DECLARATIONS////////////
float x = 0;
float y = 0;
float mousex = 0;
float mousey = 0;

float dirx = 10;
float diry = 10;
GtkWidget *window;

GtkWidget *darea;

float delta = 0.016;

float repulsion = 200000;
float friction = 4;
float criticalradius = 150;

float rayon = 10;

#define nball 5

GArray *balls;

bool catched = false;
int catchn = 0;
float catchx = 0;
float catchy = 0;

Ball *pairing = NULL;

unsigned long long lastime = 0;
//////////EVENTS//////////////////

static gboolean on_draw_event(GtkWidget *widget, cairo_t *cr, gpointer user_data)
{
  do_drawing(widget,cr);
  return FALSE;
}

static gboolean onmouse(GtkWidget *widget, GdkEventMotion *event, gpointer user_data) {
    mousex = event->x; mousey = event->y;
    return FALSE;
}

static gboolean onpress(GtkWidget *widget, GdkEventButton *event, gpointer user_data) {
    mousex = event->x; mousey = event->y;

    if (event->type == GDK_BUTTON_PRESS  &&  event->button == 3) //RIGHT
    {
      gboolean touche = false;
      for(int i = 0;i<balls->len;i++)
	{
	  Ball *bali = g_array_index(balls, Ball *, i);
	  if(inball(mousex,mousey,bali))
	    {
	      g_array_remove_index (balls,i);

	      for(int j = 0;j<bali->attached->len;j++)
		{
		  Ball *badj = g_array_index(bali->attached, Ball *, j);
		  g_array_remove_index (badj->attached,getBallIndex(badj->attached, bali));
		}
	      g_array_free(bali->attached,false);
	      free(bali);
	      
	      touche = true;
	      break;
	    }
	}
      if(!touche)addball(mousex,mousey);
      //printf("%d\n",!touche);
    }
    if (event->type == GDK_BUTTON_PRESS  &&  event->button == 2) //MID
    {
      
      for(int i = 0;i<balls->len;i++)
	{
	  Ball *bali = g_array_index(balls, Ball *, i);
	  if(inball(mousex,mousey,bali) && pairing != bali)
	    {
	      if(pairing == NULL)
		{
		  pairing = bali;
		}
	      else
		{
		  if(getBallIndex(bali->attached, pairing) == -1)
		  g_array_append_val(bali->attached,pairing);

		  if(getBallIndex(pairing->attached, bali) == -1)
		  g_array_append_val(pairing->attached,bali);
		  pairing = NULL;
		}
	      break;
	    }
	}
    }
    if (event->type == GDK_BUTTON_PRESS  &&  event->button == 1) //LEFT
    {
      for(int i = 0;i<balls->len;i++)
	{
	  Ball *bali = g_array_index(balls, Ball *, i);
	  if(inball(mousex,mousey,bali))
	    {
	      catched = true;
	      catchn = i;
	      catchx = bali->x-mousex;
	      catchy = bali->y-mousey;
	      break;
	    }
	}
    }
    
    
    
    return true;
}

static gboolean onrelease(GtkWidget *widget, GdkEventButton *event, gpointer user_data) {
    mousex = event->x; mousey = event->y;
    catched = false;
    //printf("%d\n",0);
    return true;
}

///////////MAIN////////////////////

gboolean timer_exe(GtkWidget * window)
{
  //printf("lool\n");
  gtk_widget_queue_draw (darea);
  return true;
}

int main(int argc, char *argv[])
{ 
  srand(time(NULL));

  balls = g_array_new (false, false, sizeof (Ball *));
  
  for(int i = 0;i<nball;i++)
  {
    addball(400+300*(0.5-randoma()),300+200*(0.5-randoma()));
  }

  

  gtk_init(&argc, &argv);

  window = gtk_window_new(GTK_WINDOW_TOPLEVEL);

  darea = gtk_drawing_area_new();
  gtk_container_add(GTK_CONTAINER(window), darea);
  gtk_widget_set_events (window, GDK_EXPOSURE_MASK
          | GDK_LEAVE_NOTIFY_MASK   | GDK_POINTER_MOTION_MASK | GDK_BUTTON_PRESS_MASK
          | GDK_BUTTON_RELEASE_MASK);

  g_signal_connect(G_OBJECT(darea), "draw", G_CALLBACK(on_draw_event), NULL); 
  g_signal_connect(window, "destroy",G_CALLBACK(gtk_main_quit), NULL);
  g_signal_connect(window, "motion_notify_event", G_CALLBACK(onmouse), NULL);
  g_signal_connect(window, "button-press-event", G_CALLBACK(onpress), NULL);
  g_signal_connect(window, "button-release-event", G_CALLBACK(onrelease), NULL);

  gtk_window_set_position(GTK_WINDOW(window), GTK_WIN_POS_CENTER);
  gtk_window_set_default_size(GTK_WINDOW(window), 800, 600); 
  gtk_window_set_title(GTK_WINDOW(window), "GTK window");

  gtk_widget_show_all(window);

  (void)g_timeout_add((int)(delta*1001), (GSourceFunc)timer_exe, window);
  
  gtk_main();

  return 0;
}


//////////////UTILITY FUNCTIONS//////////////

static float randoma()
{
  return (1./(float)RAND_MAX)*(float)rand();
}

static int getBallIndex(GArray *arr,Ball * b)
{
  for(int i = 0;i<arr->len;i++)
  {
    Ball *bali = g_array_index(arr, Ball *, i);
    if(bali == b)return i;
  }
  return -1;
}

Ball *bal;
static void addball(float x,float y)
{
  bal = malloc(sizeof(Ball));
  memset(bal,0,sizeof(Ball));

  bal->x = x;
  bal->y = y;
  bal->vx = 20*(0.5-randoma());
  bal->vy = 20*(0.5-randoma());
  bal->radius = 30+rayon*randoma();
  if(balls->len == 0)bal->radius=20;
  bal->r = randoma();
  bal->g = randoma();
  bal->b = randoma();
  bal->attached = g_array_new (false, false, sizeof (Ball *));
  
  //printf("%p\n",bal);
  g_array_append_val (balls, bal);
}
/*
static void ball_gravity(Ball* b1, Ball* b2)
{
  float distx = (b2->x)-(b1->x);
  float disty = (b2->y)-(b1->y);
  float distance = sqrtf(powf(distx,2.) + powf(disty,2.))+0.00001;
  float fakedist = distance;
  
  float critic = criticalradius;//powf(balls->len,0.5)*53;
  if(critic<50)critic = 50;
    
  float factor = 1;
  if(fakedist<10)fakedist=10;
  if(fakedist>critic-10)fakedist = critic-10;
  if(fakedist>critic/2)
  {
  fakedist=critic-fakedist;
  factor = -1;
  }
  float repforce = factor*repulsion/powf(fakedist,2);
  if(repforce>repulsion)repforce=repulsion;

  float forcex = (distx/distance)*repforce;
  float forcey = (disty/distance)*repforce;
  
  float power = powf((*b2).radius/rayon,2);
   
  (*b1).vx -= delta*forcex*power;
  (*b1).vy -= delta*forcey*power;


  //printf("%d \n",(int)forcex);
  //(*b2).vx += delta*forcex;
  //(*b2).vy += delta*forcey;
  
  }*/

static void ball_repulsion(Ball* b1, Ball* b2)
{
  float distx = (b2->x)-(b1->x);
  float disty = (b2->y)-(b1->y);
  float distance = sqrtf(powf(distx,2.) + powf(disty,2.))+0.00001;
  float fakedist = distance;
  if(fakedist<20)fakedist=20;

  float factor = 5;
  if(distance>200)factor = 0;

  float repforce = factor*repulsion/powf(fakedist,2);
  if(repforce>3000)repforce=3000;

  float forcex = (distx/distance)*repforce;
  float forcey = (disty/distance)*repforce;
  
  float power = powf((*b2).radius/rayon,2);
   
  (*b1).vx -= delta*forcex*power;
  (*b1).vy -= delta*forcey*power;
}

static void ball_attraction(Ball* b1, Ball* b2)
{
  float distx = (b2->x)-(b1->x);
  float disty = (b2->y)-(b1->y);
  float distance = sqrtf(powf(distx,2.) + powf(disty,2.))+0.00001;
  float fakedist = distance;

  float factor = -1;

  float repforce = factor*repulsion*powf(fakedist,2)/10000000;
  if(repforce<-3000)repforce=-3000;

  float forcex = (distx/distance)*repforce;
  float forcey = (disty/distance)*repforce;
  
  float power = powf((*b2).radius/rayon,2);
   
  (*b1).vx -= delta*forcex*power;
  (*b1).vy -= delta*forcey*power;
}

static float mimax(float x, int minx, int maxx,float r)
{
  if(x<minx+r)return minx+r;
  if(x>maxx-r)return maxx-r;
  return x;
}

static bool inball(float x,float y, Ball* b)
{
  float distx = (b->x)-x;
  float disty = (b->y)-y;
  float distance = sqrtf(powf(distx,2.) + powf(disty,2.));
  
	if(distance<=(*b).radius)return true;
  else return false;
}

static bool squarecol(float x,float y, float minx, float miny, float maxx, float maxy)
{
	if(x>maxx || x<minx || y>maxy || y<miny)return true;
  else return false;
}

static bool ball_collisions(Ball* b, int minx, int miny, int maxx, int maxy)
{
  float radi = (*b).radius;
  float x = (*b).x;
  float y = (*b).y;
  if(x+radi>maxx || x-radi<minx || y+radi>maxy || y-radi<miny)return true;
  else return false;
  
}

static void ball_walls(Ball* b, int minx, int miny, int maxx, int maxy)
{
  //(*b).vx += delta*1*(0.5-randoma());
  //(*b).vy += delta*1*(0.5-randoma());
  
  (*b).vx -= delta*friction*(*b).vx;
  (*b).vy -= delta*friction*(*b).vy;

  float oldx = (*b).x;
  float oldy = (*b).y;

  (*b).x+=(*b).vx*delta;
  if(ball_collisions(b,minx,miny,maxx,maxy))
  {
    (*b).x=mimax(oldx,minx,maxx,(*b).radius);
    (*b).vx = -(*b).vx*0.7;
  }

  (*b).y+=(*b).vy*delta;
  if(ball_collisions(b,minx,miny,maxx,maxy))
  {
    (*b).y=mimax(oldy,miny,maxy,(*b).radius);
    (*b).vy = -(*b).vy*0.7;
  }
}

static void recurSearch(GArray *curgroup, Ball *b)
{
  //printf("AAAA %f BB %d\n",b->radius,b->attached->len);
  for(int i=0;i<b->attached->len;i++)
    {
      Ball *b2 = g_array_index(b->attached,Ball *,i);
      if(!b2->grouped)
	{
	  b2->grouped = true;
	  g_array_append_val(curgroup,b2);
	  recurSearch(curgroup,b2);
	}
    }
}

/////////DRAW/////////////////

static void do_drawing(GtkWidget *widget,cairo_t *cr2)
{ 
  int w = gtk_widget_get_allocated_width (window);
  int h = gtk_widget_get_allocated_height (window);

  if(w<50)w=50;
  if(h<50)h=50;

  //GArray *checked  = g_array_new (false, false, sizeof (bool));
  for(int i = 0;i<balls->len;i++)
    g_array_index(balls, Ball *, i)->grouped = false;
    //g_array_append_val(checked,false);

  for(int i = 0;i<balls->len;i++)
    {
      if(!g_array_index(balls, Ball *, i)->grouped)
	{
	  g_array_index(balls, Ball *, i)->grouped = true;
	  
	  GArray *curgroup  = g_array_new (false, false, sizeof (Ball *));
	  g_array_append_val(curgroup,g_array_index(balls, Ball *, i));
	  
	  recurSearch(curgroup,g_array_index(balls, Ball *, i));
	  for(int j = 0;j<curgroup->len;j++)
	    {
	      for(int k = 0;k<curgroup->len;k++)
		{
		  if(j!=k)ball_repulsion(g_array_index(curgroup, Ball *, j),g_array_index(curgroup, Ball *, k));
		}
	    }
	}
    }

  //ATTRACTION
  for(int i = 0;i<balls->len;i++)
  {
    Ball *bali = g_array_index(balls, Ball *, i);
    for(int j = 0;j<bali->attached->len;j++)
      {
	Ball *balj = g_array_index(bali->attached, Ball *, j);
        ball_attraction(bali,balj);
      }
  }

  //APPLY MOVE
  for(int i = 0;i<balls->len;i++)
  {
    Ball *bali = g_array_index(balls, Ball *, i);
    ball_walls(bali,0,0,w,h);
    if(catched && catchn == i)
    {
    	bali->x = mousex+catchx;
    	bali->y = mousey+catchy;
    }
  }



  //create a gtk-independant surface to draw on
  cairo_surface_t *cst = cairo_image_surface_create(CAIRO_FORMAT_ARGB32, w, h);
  cairo_t *cr = cairo_create(cst);
  
  //do some time-consuming drawing
  cairo_set_source_rgb (cr, .2,.2,.2);
  cairo_paint(cr);


  
  //DRAW LINES
  cairo_set_line_width(cr, 1.5);
  for(int i = 0;i<balls->len;i++)
  {
    Ball *bali = g_array_index(balls, Ball *, i);
    for(int j = 0;j<bali->attached->len;j++)
      {
	Ball *balj = g_array_index(bali->attached, Ball *, j);

	cairo_set_source_rgb(cr,0,0,0);
	
	cairo_move_to(cr, bali->x, bali->y);
	cairo_line_to(cr, balj->x, balj->y);
	cairo_stroke(cr);
      }
  }
  cairo_move_to(cr, 0, 0);
  

  //DRAW CIRCLES
  for(int i = 0;i<balls->len;i++)
  {
    Ball *bali = g_array_index(balls, Ball *, i);
    cairo_set_source_rgb(cr,bali->r,bali->g,bali->b);
    cairo_arc(cr, bali->x, bali->y, bali->radius, 0, 2 * M_PI);
    cairo_fill(cr);

    cairo_set_source_rgb(cr,0,0,0);
    cairo_arc(cr, bali->x, bali->y, bali->radius, 0, 2 * M_PI);
    cairo_stroke(cr);
  }




  cairo_destroy(cr);

  
  //cairo_t *cr_pixmap = cairo_create(cst);
  cairo_set_source_surface (cr2, cst, 0, 0);
  cairo_paint(cr2);
  //cairo_destroy(cr_pixmap);
  cairo_surface_destroy(cst);

  struct timeval tv;
  gettimeofday(&tv, NULL);
  unsigned long long millisecondsSinceEpoch =
    (unsigned long long)(tv.tv_sec) * 1000 +
    (unsigned long long)(tv.tv_usec) / 1000;
  printf("%llu\n", millisecondsSinceEpoch-lastime);
  lastime = millisecondsSinceEpoch;

  //printf("%d\n",widget==darea);
}
