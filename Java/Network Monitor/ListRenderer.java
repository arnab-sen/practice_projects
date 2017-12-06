import java.awt.Color;
import java.awt.Component;

import javax.swing.BorderFactory;
import javax.swing.JLabel;
import javax.swing.JList;
import javax.swing.ListCellRenderer;

public class ListRenderer extends JLabel implements ListCellRenderer {
	private Color darkDarkGray = new Color(50, 50, 60);
	private Color unknownColor = new Color(177, 249, 252);
	private Color connectedColor = new Color(0, 210, 20);
	private Color disconnectedColor = new Color(200, 50, 50);
	
	public ListRenderer() {
		setOpaque(true);
	}
	
	@Override
	public Component getListCellRendererComponent(JList list, 
												  Object value,
												  int index, 
												  boolean isSelected,
												  boolean cellHasFocus) {
		
		if (value == "unknown") {
			if (isSelected | cellHasFocus)
				setBorder(BorderFactory.createLineBorder(unknownColor));
			setBackground(unknownColor);
		} else if (value == "OK "){
			if (isSelected | cellHasFocus)
				setBorder(BorderFactory.createLineBorder(connectedColor));
			setBackground(connectedColor);
			setBorder(BorderFactory.createLineBorder(darkDarkGray));
		} else if (value == "DISCONNECTED ") {
			if (isSelected | cellHasFocus)
				setBorder(BorderFactory.createLineBorder(disconnectedColor));
			setBackground(disconnectedColor);
			setBorder(BorderFactory.createLineBorder(darkDarkGray));
		}
		return this;
	}

}
