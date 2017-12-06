import java.util.ArrayList;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.awt.*;
import java.awt.event.*;
import java.io.File;
import javax.swing.*;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class NetworkMonitor extends JFrame{
	private JLabel connectionStatus;
	private JLabel connected;
	private JButton tryConnection;
	private Connection connection;
	private boolean isConnected = false;
	private String connectionText = null;
	private Font regularFont, boldFont, logFont;
	private JLabel connectionLogLabel;
	private JList<String> connectionLog;
	private JScrollPane connectionLogScrollPane;
	private JPanel connectionPanel;
	private JList<String> overviewTimes;
	private JList<String> overviewBlocks;
	private Timer timer;
	private Timer scrollTimer;
	private ActionListener connectionCheckAction;
	private Color mainColor = Color.GRAY;
	private Color teal = new Color(24, 112, 107);
	private Color darkDarkGray = new Color(50, 50, 60);
	private Color darkBlue = new Color(29, 56, 129);
	private Color limeGreen = new Color(18, 254, 53);
	private String currentDateTime;
	private String currentTime;
	private int lastMinutesTotal = 0;
	
	
	public NetworkMonitor() {
		super("Network Monitor");
		//setLayout(new FlowLayout());
		setLayout(new BorderLayout());
		setSize(750, 726);
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		regularFont = new Font("", Font.PLAIN, 18);
		boldFont = new Font("", Font.BOLD, 18);
		logFont = new Font("Lucida Console", Font.PLAIN, 14);
		
		setupConnectionChecker();
		setupConnectionLog();
		setupConnectionTimer();
		setupMenu();
		setupOverview();
		
		timer.start();
		scrollTimer.start();
		
		//connectionPanel.setBackground(mainColor);
		
		setLocationRelativeTo(null); // center the window
		setVisible(true);
	}
	
	private void setupMenu() {
		JMenuBar menuBar = new JMenuBar();
		menuBar.setBorder(BorderFactory.createLineBorder(Color.black));
		menuBar.setBackground(darkDarkGray);
		setJMenuBar(menuBar);
		JMenu fileMenu = new JMenu("File");
		fileMenu.setForeground(Color.white);
		fileMenu.setBackground(darkDarkGray);
		JMenuItem consoleBGMenu = new JMenuItem("Console Background Colour");
		JMenuItem consoleFGMenu = new JMenuItem("Console Foreground Colour");

		consoleBGMenu.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				Color userColor = getColorChoice(connectionLog.getBackground());
				// JColorChooser returns null on Cancel
				if (userColor != null) {
					connectionLog.setBackground(userColor);
				}
			}	
		});
		consoleFGMenu.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				Color userColor = getColorChoice(connectionLog.getForeground());
				// JColorChooser returns null on Cancel
				if (userColor != null) {
					connectionLog.setForeground(userColor);
				}
			}	
		});
		
		menuBar.add(fileMenu);
		fileMenu.add(consoleBGMenu);
		fileMenu.add(consoleFGMenu);
		fileMenu.setBorder(BorderFactory.createLineBorder(darkDarkGray));
		
		for (int i = 0; i < fileMenu.getItemCount(); i++) {
			fileMenu.getItem(i).setBackground(darkDarkGray);
			fileMenu.getItem(i).setForeground(Color.white);
			fileMenu.getItem(i).setBorder(BorderFactory.createLineBorder(Color.black));
		}
	}
	
	private void setupConnectionChecker() {
		connectionPanel = new JPanel();
		connection = new Connection();
		connectionStatus = new JLabel("Connection Status: ");
		connectionStatus.setFont(regularFont);
		connectionStatus.setForeground(Color.white);
		//add(connectionStatus, BorderLayout.PAGE_START);
		connectionPanel.add(connectionStatus);
		connectionPanel.setBackground(darkDarkGray);
		connected = new JLabel("Connecting... ");
		connected.setForeground(Color.white);
		connected.setFont(boldFont);
		//add(connected, BorderLayout.PAGE_START);
		connectionPanel.add(connected);
		tryConnection = new JButton("Connect");
		tryConnection.setEnabled(true);
		tryConnection.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				checkConnection();
			}
		});
		//add(tryConnection);
		//connectionPanel.add(tryConnection);
		add(connectionPanel, BorderLayout.PAGE_START);
	}
	
	private void setupConnectionLog() {
		connectionLogLabel = new JLabel("Connection Log:");
		connectionLogLabel.setFont(regularFont);
		//add(connectionLogLabel, BorderLayout.LINE_START);
		connectionLog = new JList<String>(new DefaultListModel<String>());
		connectionLog.setFont(logFont);
		connectionLog.setBackground(Color.black);
		connectionLog.setForeground(limeGreen);
		connectionLog.setVisibleRowCount(10);
		connectionLog.setFixedCellHeight(20);
		connectionLog.setFixedCellWidth(450);
		connectionLogScrollPane = new JScrollPane(connectionLog);
		connectionLogScrollPane.setBorder(BorderFactory.createLineBorder(Color.black));
		add(connectionLogScrollPane, BorderLayout.LINE_END);
		
		// Add placeholder borders
		JPanel fillerPanel = new JPanel();
		fillerPanel.setBackground(darkDarkGray);
		fillerPanel.setBorder(BorderFactory.createLineBorder(Color.black));
		add(fillerPanel, BorderLayout.PAGE_END);
		//add(fillerPanel, BorderLayout.LINE_START);
		//add(fillerPanel, BorderLayout.LINE_END);
	}
	
	private void setupConnectionTimer() {
		connectionCheckAction = new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				checkConnection();
				if (connectionText != null) {
					getCurrentDateTime();
					String status = currentDateTime + "-- " + connectionText;
					((DefaultListModel)(connectionLog.getModel())).addElement(status);		
					addOverviewBlock();
				}
			}
		};
		
		timer = new Timer(3000, connectionCheckAction);
		scrollTimer = new Timer(0, new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				// Have the scroll bar automatically scroll to the bottom when
				// not in use
				JScrollBar scrollBar = connectionLogScrollPane.getVerticalScrollBar();
				if (!scrollBar.getValueIsAdjusting()) {
					scrollBar.setValue(scrollBar.getMaximum());
				}
			}
		});
	}
	
	private void setupOverview() {
		overviewTimes = new JList<String>(new DefaultListModel<String>());
		overviewTimes.setVisibleRowCount(12);
		overviewTimes.setFixedCellHeight(28);
		overviewTimes.setFixedCellWidth(47);
		overviewTimes.setBackground(darkDarkGray);
		overviewTimes.setForeground(Color.white);
		JScrollPane overviewTimesSP = new JScrollPane(overviewTimes);
		overviewTimesSP.setBorder(BorderFactory.createLineBorder(Color.black));
		add(overviewTimesSP, BorderLayout.LINE_START);
		String[] times = {"08", "09", "10", "11", "12", "13", "14", "15", "16",
						  "18", "19", "20", "21", "22", "23", "01", "02", "03",
						  "04", "05", "06", "07"};
		for (String time : times) {
			((DefaultListModel)(overviewTimes.getModel())).addElement("  " + time + ":00");
		}	
			
		overviewBlocks = new JList<String>(new DefaultListModel<String>());
		overviewBlocks.setVisibleRowCount(12);
		overviewBlocks.setFixedCellHeight(7);
		overviewBlocks.setFixedCellWidth(150);
		//overviewTimes.setBackground(limeGreen);
		//overviewTimes.setForeground(Color.black);
		JScrollPane overviewBlocksSP = new JScrollPane(overviewBlocks);
		overviewBlocksSP.setBorder(BorderFactory.createLineBorder(Color.black));
		add(overviewBlocksSP, BorderLayout.CENTER);
		
		/* Test blocks
		for (int i = 0; i < (times.length * 4); i++) {
			String toAdd;
			if (i % 3 == 0) {
				toAdd = "disconnected";
			} else {
				toAdd = "connected";
			}
			((DefaultListModel)(overviewBlocks.getModel())).addElement(toAdd);
		}
		*/

		ListRenderer r = new ListRenderer();
		overviewBlocks.setCellRenderer(r);
		setupOverviewBlocks();	
	}
	
	private Color getColorChoice(Color defaultColor) {
		Color userColor = JColorChooser.showDialog(connectionPanel, "", defaultColor);
		return userColor;
	}
	
	public void checkConnection() {
		SwingWorker worker = new SwingWorker<Void, Boolean>() {
			@Override
			public Void doInBackground() {
				while (true) {
					isConnected = connection.isConnected();
					updateConnectionStatus();
				}
				//return null;
			}
		};
		worker.execute();
		//connection.execute();
		/*
		try {
			//isConnected = connection.get();
			isConnected = connection.isConnected();
		} catch (Exception e) {
			e.printStackTrace();
		}
		updateConnectionStatus();
		*/
	}
	
	private void updateConnectionStatus() {
		if (isConnected) {
			connectionText = "OK ";
			connected.setText(connectionText);
			connected.setForeground(limeGreen);
		} else {
			connectionText = "DISCONNECTED ";
			connected.setText(connectionText);
			connected.setForeground(Color.red);
		}
	}
	
	public void getCurrentDateTime() {
		DateTimeFormatter dtf = DateTimeFormatter.ofPattern("dd MMMM yyyy -- HH:mm:ss ");
		LocalDateTime now = LocalDateTime.now();
		currentDateTime = dtf.format(now);
		currentTime = currentDateTime.substring(currentDateTime.indexOf("--") + 3, currentDateTime.length());			
	}
		
	private void setupOverviewBlocks() {
		/*
		 * Adds white overviewBlock elements up until the current time's index
		 */
		// Convert time to overviewBlock index, which starts at [0] = 08:00, [1] = 08:15, etc
		
		int minutesTotal = getCurrentMinutesTotal();
		int startIndex = (minutesTotal - 480) / 15;
		
		for (int i = 0; i < startIndex; i++) {
			((DefaultListModel)(overviewBlocks.getModel())).addElement("unknown");
		}
		
		if (lastMinutesTotal > 0)
			lastMinutesTotal = minutesTotal;
		
		//((DefaultListModel)(overviewBlocks.getModel())).addElement("OK ");
	}
	
	private int getCurrentMinutesTotal() {
		String hoursAndSeconds;
		getCurrentDateTime();
		int currentHour = Integer.parseInt(currentTime.substring(0, currentTime.indexOf(":")));
		hoursAndSeconds = currentTime.substring(currentTime.indexOf(":") + 1, currentTime.length());
		int currentMinutes = Integer.parseInt(hoursAndSeconds.substring(0, hoursAndSeconds.indexOf(":")));
		
		return currentHour * 60 + currentMinutes;
	}
	
	private void addOverviewBlock() {
		int minutesTotal = getCurrentMinutesTotal();
		if ((minutesTotal - lastMinutesTotal) >= 15) { 
			lastMinutesTotal = minutesTotal;
			((DefaultListModel)(overviewBlocks.getModel())).addElement(connectionText);
			//System.out.println("New block added at " + currentTime);
		} else if (connectionText.startsWith("DISCONNECTED")) {
			int lastIndex = ((DefaultListModel)(overviewBlocks.getModel())).getSize() - 1;
			((DefaultListModel)(overviewBlocks.getModel())).set(lastIndex, connectionText);
		}
	}
	
	public static void main(String[] args) {
		
	}

}
