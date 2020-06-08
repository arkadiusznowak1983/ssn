package ssn7;
import java.awt.EventQueue;
import java.awt.Graphics;
import java.util.Random;

import javax.swing.JFrame;
import javax.swing.JPanel;
import java.awt.Color;
import javax.swing.border.LineBorder;

import com.sun.corba.se.impl.orbutil.graph.Graph;
import com.sun.prism.shader.DrawCircle_Color_AlphaTest_Loader;
import javax.swing.JButton;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import javax.swing.JLabel;
import java.awt.Font;
import javax.swing.SwingConstants;

public class SimpleNeuralNetwork
{

	private JFrame frame;
	private static XYGraph graphx;
	/**
	 * NeuralCell Object
	 */
	private static NeuralCell cell;
	private JLabel x_weight;
	private JLabel y_weight;
	
	
	/**
	 * Launch the application.
	 */
	public static void main(String[] args)
	{
		EventQueue.invokeLater(new Runnable()
		{
			public void run()
			{
				try
				{
					SimpleNeuralNetwork window = new SimpleNeuralNetwork();
					window.frame.setVisible(true);
				}
				catch (Exception e)
				{
					e.printStackTrace();
				}
			}
		});
		
		
	}
	
	/**
	 * Create the application.
	 */
	public SimpleNeuralNetwork()
	{
		initialize();
		
		/**
		 * Creating the cell.
		 * Override the finalizeData function for unique output.
		 */
		cell = new NeuralCell()
		{
			@Override
			public double finalizeData(double membranePotential)
			{
				if(membranePotential > 0)
					return 1;
				else
				if(membranePotential < 0)
					return -1;
				else
					return 0;
			}
		};
		
		/**
		 * Adding two dendrytes and synapses for input.
		 */
		cell.addInput(2);
		
		/**
		 * Setting random weights.
		 * Between 0 and 1.
		 */
		Random rand = new Random();
		double rx = rand.nextDouble();
		double ry = rand.nextDouble();
		cell.setInputWeight(0, rx);
		cell.setInputWeight(1, ry);
		
		x_weight.setText(Double.toString(rx));
		y_weight.setText(Double.toString(ry));
	}
	

	/**
	 * Initialize the contents of the frame.
	 */
	private void initialize()
	{
		frame = new JFrame();
		frame.setBounds(100, 100, 599, 420);
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.getContentPane().setLayout(null);
		
		graphx = new XYGraph();
		graphx.setBorder(new LineBorder(new Color(0, 0, 0)));
		graphx.setBackground(Color.WHITE);
		graphx.setBounds(10, 11, 360, 360);
		frame.getContentPane().add(graphx);
		
		JButton btnAddPoint = new JButton("Add 500 Points");
		btnAddPoint.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				
				for(int i = 1; i<=500; i++)
					addRandomPoint();
			}
		});
		btnAddPoint.setBounds(408, 55, 144, 23);
		frame.getContentPane().add(btnAddPoint);
		
		JLabel lblWagaX = new JLabel("Waga X");
		lblWagaX.setHorizontalAlignment(SwingConstants.CENTER);
		lblWagaX.setFont(new Font("Tahoma", Font.PLAIN, 16));
		lblWagaX.setBounds(408, 89, 58, 23);
		frame.getContentPane().add(lblWagaX);
		
		JLabel lblWagaY = new JLabel("Waga Y");
		lblWagaY.setHorizontalAlignment(SwingConstants.CENTER);
		lblWagaY.setFont(new Font("Tahoma", Font.PLAIN, 16));
		lblWagaY.setBounds(494, 89, 58, 23);
		frame.getContentPane().add(lblWagaY);
		
		x_weight = new JLabel("x");
		x_weight.setHorizontalAlignment(SwingConstants.CENTER);
		x_weight.setFont(new Font("Tahoma", Font.PLAIN, 16));
		x_weight.setBounds(408, 114, 58, 23);
		frame.getContentPane().add(x_weight);
		
		y_weight = new JLabel("y");
		y_weight.setHorizontalAlignment(SwingConstants.CENTER);
		y_weight.setFont(new Font("Tahoma", Font.PLAIN, 16));
		y_weight.setBounds(494, 114, 58, 23);
		frame.getContentPane().add(y_weight);
	
	}
	
     private void addRandomPoint()
     {
     	// Generate two numbers
     	Random r = new Random();
     	int x = r.nextInt()%180;
     	int y = r.nextInt()%180;
     	
     	// Pass them to the neural cell
     	cell.setInputData(0, x);
     	cell.setInputData(1, y);
     	
     	// Get the output
     	int result = (int)cell.getOutput();
     	
     	// Draw appropriate point colour
     	if(result == 1)
     		graphx.drawPoint(x, y, Color.BLUE);
     	else
     	if(result == -1)
     		graphx.drawPoint(x, y, Color.RED);
     }
	
     class XYGraph extends JPanel
     {
     	/**
     	 * Variables which contains info about 
     	 * currently added point.
     	 */
     	Color clr;
     	int x_var;
     	int y_var;
     	
     	/**
     	 * Override to write custom point.
     	 */
     	@Override
     	protected void paintComponent(Graphics g)
     	{
     		super.paintComponent(g);
     		g.setColor(clr);
     		if(x_var != 0 && y_var != 0)
     			g.fillRect(x_var, y_var, 4, 4);
     		paintCross(g);
     	}
     	
     	/**
     	 * Yet another smart function to draw 
     	 * a cross on the component.
     	 * @param g
     	 */
     	private void paintCross(Graphics g)
     	{
     		g.setColor(Color.BLACK);
     		g.fillRect(180, 0, 1, 360);
     		g.drawLine(176, 8, 180, 0);
     		g.drawLine(184, 8, 180, 0);
     		
     		g.fillRect(0, 180, 360, 1);
     		g.drawLine(352, 176, 360, 180);
     		g.drawLine(352, 184, 360, 180);
     		g.drawString("0", 183, 193);
     	}
     	
     	/**
     	 * Writes a point at selected coordinates 
     	 * with selected colour.
     	 * @param x coordinate X
     	 * @param y coordinate Y
     	 * @param clr selected colour
     	 */
     	public void drawPoint(int x, int y, Color clr)
     	{
     		
     		x+=180;
     		y+=180;
     		y=360-y;
     		x_var = x;
     		y_var = y;
     		this.clr = clr;
     		paintImmediately(x,y,4,4);
     	}
     }
}