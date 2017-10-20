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


const int default_precision_graph = 1024;
int precision_graph = 1024; //in ms, relative to default scaleX

float rayon = 2;

const float defaultscaleX = 64;
float scaleX = 64; //=1 for 1px on graph per second; =1000 for 1px on graph per millisecond etc

float scaleXMIN = 1;
float scaleXMAX = 512;

float marginX = 80;
float marginY = 30;


///////STRUCS///////////

typedef struct Dot Dot;

struct Dot
{
  float x;
  float y;
  Dot *prevdot;
  float r;
  float g;
  float b;
};

/////////FUNCTIONS DECLARATIONS////////////
static gboolean onscroll(GtkWidget *widget, GdkEventScroll *event, gpointer user_data);

static float randoma();
static void sleep_ms(int milliseconds);
static void do_drawing(cairo_t *cr);
static void addot(float x,float y);
static void plotnewdata(float delay,float size);
static void demo();
static void updateGraph();

/////////VARIABLES DECLARATIONS////////////
GtkWidget *window;

GArray *dots;

float lastdatatime = 0;

float maxrange = 5000;

//////////EVENTS//////////////////

static gboolean on_draw_event(GtkWidget *widget, cairo_t *cr, gpointer user_data)
{
  do_drawing(cr);
  return FALSE;
}

static gboolean onscroll(GtkWidget *widget, GdkEventScroll *event, gpointer user_data)
{
  if(event->direction==1)
  {
    scaleX*=0.5;
    if(scaleX<=scaleXMIN)scaleX=scaleXMIN;
    precision_graph=default_precision_graph*(defaultscaleX/scaleX);
  }
  else if(event->direction==0)
  {
    scaleX*=2;
    if(scaleX>=scaleXMAX)scaleX=scaleXMAX;
    precision_graph=default_precision_graph*(defaultscaleX/scaleX);
  } 
  return FALSE;
}

///////////MAIN////////////////////

int main(int argc, char *argv[])
{ 
  srand(time(NULL));

  dots = g_array_new (false, false, sizeof (Dot *));
  
  GtkWidget *darea;

  gtk_init(&argc, &argv);

  window = gtk_window_new(GTK_WINDOW_TOPLEVEL);

  darea = gtk_drawing_area_new();
  gtk_container_add(GTK_CONTAINER(window), darea);
  gtk_widget_set_events (window, GDK_EXPOSURE_MASK
          | GDK_LEAVE_NOTIFY_MASK   | GDK_POINTER_MOTION_MASK | GDK_BUTTON_PRESS_MASK | GDK_SCROLL_MASK
          | GDK_BUTTON_RELEASE_MASK);

  g_signal_connect(G_OBJECT(darea), "draw", G_CALLBACK(on_draw_event), NULL); 
  g_signal_connect(window, "scroll-event", G_CALLBACK(onscroll), NULL);

  gtk_window_set_position(GTK_WINDOW(window), GTK_WIN_POS_CENTER);
  gtk_window_set_default_size(GTK_WINDOW(window), 800, 600); 
  gtk_window_set_title(GTK_WINDOW(window), "GTK window");

  gtk_widget_show_all(window);

  gtk_main();

  return 0;
}


//////////////UTILITY FUNCTIONS//////////////

static float randoma()
{
  return (1./(float)RAND_MAX)*(float)rand();
}

Dot *bal;
static void addot(float x,float y)
{
  bal = malloc(sizeof(Dot));
  memset(bal,0,sizeof(Dot));

  bal->x = x;
  bal->y = y;
  bal->r = 0;
  bal->g = 0;
  bal->b = 0.5;
  if(dots->len > 0)
  {
    bal->prevdot = g_array_index(dots, Dot *, (dots->len)-1);
  }
  else bal->prevdot=NULL;
  
  //printf("%p\n",bal);
  g_array_append_val (dots, bal);

  Dot *first = g_array_index(dots, Dot *, 0);
  while(first->x < bal->x*scaleXMIN - maxrange)
  {
    g_array_remove_index(dots,0);
    first = g_array_index(dots, Dot *, 0);
  }
}

static void plotnewdata(float delay, float size)
{
  addot((lastdatatime+delay),-(size/delay));
  lastdatatime+=delay;
  updateGraph();//REMOVE THIS IF YOU CALL THE UPDATE ELSEWHERE
}

static void sleep_ms(int milliseconds)
{
    struct timespec ts;
    ts.tv_sec = milliseconds / 1000;
    ts.tv_nsec = (milliseconds % 1000) * 1000000;
    nanosleep(&ts, NULL);
}

/////////DRAW/////////////////



static void do_drawing(cairo_t *cr)
{ 
  int w = gtk_widget_get_allocated_width (window);
  int h = gtk_widget_get_allocated_height (window);

  if(w<50)w=50;
  if(h<50)h=50;

  float decalagex = 0; //How much to offset the drawing

  if(dots->len>0)decalagex = w-((g_array_index(dots, Dot *, (dots->len)-1)->x)*scaleX+marginX+20);
  
  if(decalagex>0)decalagex=0;

  float basedecalx = marginX;
  float basedecaly = h-marginY;

  decalagex+=basedecalx; //for the left margin
  float decalagey = basedecaly; //To center on the y axis, with the bottom margin
  

  float maxheight = 0;
  for(int i = 0;i<dots->len;i++)
  {
    Dot *bali = g_array_index(dots, Dot *, i);
    if(-bali->y>maxheight)maxheight=-bali->y;
  }
  float scaleY = (h-marginY-h/5)/maxheight;
  
  //ARROWS
  cairo_move_to(cr, marginX, h-marginY);
  cairo_line_to(cr, w-30, h-marginY);
  cairo_stroke(cr);

  cairo_move_to(cr, w-30, h-marginY);
  cairo_line_to(cr, w-30-7, h-marginY-7);
  cairo_stroke(cr);

  cairo_move_to(cr, w-30, h-marginY);
  cairo_line_to(cr, w-30-7, h-marginY+7);
  cairo_stroke(cr);

  ///

  cairo_move_to(cr, marginX, h-marginY);
  cairo_line_to(cr, marginX, marginY);
  cairo_stroke(cr);

  cairo_move_to(cr, marginX, marginY);
  cairo_line_to(cr, marginX-7, marginY+7);
  cairo_stroke(cr);

  cairo_move_to(cr, marginX, marginY);
  cairo_line_to(cr, marginX+7, marginY+7);
  cairo_stroke(cr);

  ///

  cairo_set_font_size(cr, 20);
  
  //cairo_move_to(cr, marginX*0.2, h-marginY*0.2);
  //cairo_show_text(cr, "0"); 
  
  cairo_move_to(cr, marginX*0.2, 20);
  cairo_show_text(cr, "kBps"); 

  cairo_move_to(cr, w-100, h-marginY*0.2);
  cairo_show_text(cr, "time(s)"); 


  //LABEL TIME AXE
  float mintime = (basedecalx-decalagex)/scaleX*1000/precision_graph;
  float maxtime = mintime+(w-marginX-80)/scaleX*1000/precision_graph;

  int mint = (int)mintime+1;
  int maxt = (int)maxtime;

  cairo_set_font_size(cr, 12);
  for(int i = mint;i<maxt;i++)
  {

    char output[5];
    
    snprintf(output, 5, "%f", (float)i*precision_graph/1000);

    cairo_move_to(cr, decalagex+i*scaleX/1000*precision_graph, h-marginY+3);
    cairo_line_to(cr, decalagex+i*scaleX/1000*precision_graph, h-marginY-3);
    cairo_stroke(cr);

    cairo_move_to(cr, decalagex+i*scaleX/1000*precision_graph-10, h-marginY*0.3);
    cairo_show_text(cr, output); 
  }

  //LABEL KBPS AXE
  float minkb = 0;
 
  float maxkb = (h-marginY-50)/scaleY*1000;
  int precisionkb = (int)(maxkb/10);
  maxkb/=precisionkb;

  int mink = (int)minkb+1;
  int maxk = (int)maxkb;

  cairo_set_font_size(cr, 12);
  for(int i = mink;i<maxk;i++)
  {

    char output[7];
    
    snprintf(output, 7, "%d", (int)i*precisionkb/1000);

    cairo_move_to(cr, marginX-3, h-marginY-i*scaleY/1000*precisionkb);
    cairo_line_to(cr, marginX+3, h-marginY-i*scaleY/1000*precisionkb);
    cairo_stroke(cr);

    cairo_move_to(cr, 20,  h-marginY-i*scaleY/1000*precisionkb+5);
    cairo_show_text(cr, output); 
  }



  if(dots->len>0)
  {
    float maxtime = (g_array_index(dots, Dot *, (dots->len)-1)->x)*scaleX;
    
  }
  ///END ARROWS

  for(int i = 0;i<dots->len;i++)
  {

    Dot *bali = g_array_index(dots, Dot *, i);

    if (decalagex+bali->x*scaleX>basedecalx)
    {
      //lines
      if(bali->prevdot && decalagex+bali->prevdot->x*scaleX>basedecalx)
      {
        cairo_set_source_rgb(cr,0,0,0);
        
        cairo_move_to(cr, decalagex+(scaleX*bali->x), scaleY*bali->y+decalagey);
        cairo_line_to(cr, decalagex+(scaleX*bali->prevdot->x), scaleY*bali->prevdot->y+decalagey);
        cairo_stroke(cr);
    
        cairo_move_to(cr, 0, 0);
      }
      
      //dots
      cairo_set_source_rgb(cr,bali->r,bali->g,bali->b);
      cairo_arc(cr, decalagex+(scaleX*bali->x), scaleY*bali->y+decalagey, rayon, 0, 2 * M_PI);
      cairo_fill(cr);
    }
    
  }
  
  
  demo();// REMOVE FOR NORMAL USE
}


static void updateGraph()
{
  gtk_widget_queue_draw (window);
}

static void demo()
{
  float randtime = 0.1*randoma(); // in sec
  if(randoma()>0.97)randtime+=0.5; //huge gap simulation
  float randdata = (1000+((randoma()-0.5)*300))*randtime; //in kb (in average, the resulting bandwidth is 1Mbps)
  printf("delay : %.6f sec\n", randtime);
  printf("size : %.3f kb\n", randdata);
  sleep_ms(1000*randtime);

  plotnewdata(randtime,randdata);
}


/*
To use,remove the "demo();" from do_drawing, and call plotnewdata() to add points to the graph.
To update the window manually instead of after each plot, call updateGraph() yourself 
and remove the last line from plotnewdata
*/