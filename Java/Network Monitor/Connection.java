import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import javax.swing.SwingWorker;

// Boolean and Void are object wrappers of boolean and void
public class Connection implements Runnable {
	private static URLConnection connection;
	public boolean isConnected;

	public boolean isConnected() {
		try {			
			connection = new URL("https://www.google.com").openConnection();
			connection.connect();
			return true;
		} catch (MalformedURLException e) {
			e.printStackTrace();
			throw new RuntimeException(e);
		} catch (IOException e) {
			return false;
		}
	}
	
	public void run() {
		isConnected = isConnected();
	}
	
	public static void main(String[] args) {
		/*
		boolean connected = Connection.isConnected();
		if (connected) {
			System.out.println("Connected!");
			
		} else {
			System.out.println("Not connected");
		}
		*/
	}

}
