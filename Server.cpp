#include "thread.h"
#include "socketserver.h"
#include <stdlib.h>
#include <time.h>
#include <list>
#include <pthread.h>
#include <vector>
#include <string>

class GameThread: public Thread {
private:
  Socket sP1;
  Socket sP2;
  int* grimReaper;
public:
  GameThread(Socket const & sPa, Socket const & sPb, int* grimReaper): Thread(true), sP1(sPa), sP2(sPb), grimReaper(grimReaper) {};
  long ThreadMain(void) {
    std::string message = "";
    BePolite();

    try {
      //send a start message to both players
      ByteArray player1("player1,0,0,");
      ByteArray player2("player2,0,0,");
      sP1.Write(player1);
      sP2.Write(player2);

      while(*grimReaper) {
	//read the data from the client
	ByteArray byteMessage;

	FlexWait waiter(2, &sP1, &sP2);
	Blockable * result = waiter.Wait();
	if (result == &sP1) {
	  int read = sP1.Read(byteMessage);

	  if(read == -1) {
	    std::cout << "Error detected" << std::endl;
	    break;
	  } else if (read == 0) {
	    std::cout << "Client disconnected" << std::endl;
	    break;
	  }
	  
	  //send the data from player 2 to player1
	  sP2.Write(byteMessage);
	}
	if (result == &sP2) {
	  int read = sP2.Read(byteMessage);

	  if(read == -1) {
	    std::cout << "Error detected" << std::endl;
	    break;
	  } else if (read == 0) {
	    std::cout << "Client disconnected" << std::endl;
	    break;
	  }

	  //send the data from player 1 to player2
	  sP1.Write(byteMessage);
	}

	if (byteMessage.ToString() == "quit") {
	  message = "quit";
	  std::cout << "Client has quit the game" << std::endl;
	}
      }
      std::cout << "While you're dying I'll be still alive" << std::endl;

    }
    catch(...) {
      std::cout << "Caught unexpected exception " << std::endl;
    }
  };

};

class ServerThread: public Thread {
private:
  int* grimReaper;
  std::vector<GameThread*>* threadSalesman;

public:  
  ServerThread(int* grimReaper, std::vector<GameThread*>* threadSalesman): grimReaper(grimReaper), threadSalesman(threadSalesman) {};

  long ThreadMain(void) {
    BePolite();
    std::cout << "I am a server!" << std::endl;

    try {
      //set the port number
      int port = 2003;

      //create the Server Socket
      SocketServer socketButler(port);

    
      int socketCounter = 0;

      while(*grimReaper){
	//wait for a connection and create a new socket
	Socket socketPlayer1(socketCounter++);

	socketPlayer1 = socketButler.Accept();

	Socket socketPlayer2(socketCounter++);

	socketPlayer2 = socketButler.Accept();

	//create a new thread
	threadSalesman->push_back( new GameThread(socketPlayer1, socketPlayer2, grimReaper));
				    
	(*threadSalesman)[threadSalesman->size() - 1]->Start();
      }
    }

    catch(...) {
      std::cout << "Caught unexpected exception " << std::endl;
    }
    std::cout <<  "I'm making a note here: HUGE SUCCESS." << std::endl;
  }
};

int main(void)
{
    try
    {
      //create a vector to hold the threads
      std::vector<GameThread*> threadSalesman;

      //if this changes to 0 a thread has asked the server to die
      int grimReaper = 1;

      //create a thread to hold the server
      ServerThread theServer(&grimReaper, &threadSalesman);

      //start the server thread
      theServer.Start();

      //check if the thread should die twice a second
      std::string message = "";
      while (message != "quit") {
	std::cin >> message;
      }

      //kill the server thread
      grimReaper = 0;
      theServer.Stop();
      std::cout << threadSalesman.size() << std::endl;

      for(int i=0; i<threadSalesman.size(); i++) {
	threadSalesman[i]->Stop();
	delete threadSalesman[i];
      }

      std::cout << threadSalesman.size();
    }
    catch(...)
    {
        std::cout << "Caught unexpected exception" << std::endl;
    }
}
