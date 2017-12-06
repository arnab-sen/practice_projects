import javax.swing.SwingUtilities;

public class RunNetworkMonitor implements Runnable {
	public void run() {
		NetworkMonitor n = new NetworkMonitor();
	}
	public static void main(String[] args) {
		SwingUtilities.invokeLater(new RunNetworkMonitor());
	}

}
