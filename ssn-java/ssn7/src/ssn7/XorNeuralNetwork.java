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

public class XorNeuralNetwork
{

	private JFrame frame;
	private static XYGraph graphx;
	/**
	 * NeuralCell Object
	 */
	private static SigmaNeuralCell cell_1_1;
	private static SigmaNeuralCell cell_1_2;
	private static SigmaNeuralCell cell_2_1;
	private JLabel x_weight_1_1, x_weight_1_2, x_weight_2_1;
	private JLabel y_weight_1_1, y_weight_1_2, y_weight_2_1;
	
	
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
					XorNeuralNetwork window = new XorNeuralNetwork();
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
	public XorNeuralNetwork()
	{
		initialize();
		
		//
 		cell_1_1 = new SigmaNeuralCell();
		cell_1_1.addInputs(2);

		cell_1_2 = new SigmaNeuralCell();
		cell_1_2.addInputs(2);

		cell_2_1 = new SigmaNeuralCell();
		cell_2_1.addInputs(2);
		
		cell_1_1.setRandomWeights();
		cell_1_2.setRandomWeights();
		cell_2_1.setRandomWeights();
		
		x_weight_1_1.setText(Double.toString(cell_1_1.getInputWeight(0)));
		y_weight_1_1.setText(Double.toString(cell_1_1.getInputWeight(1)));
		
		x_weight_1_2.setText(Double.toString(cell_1_2.getInputWeight(0)));
		y_weight_1_2.setText(Double.toString(cell_1_2.getInputWeight(1)));
		
		x_weight_2_1.setText(Double.toString(cell_2_1.getInputWeight(0)));
		y_weight_2_1.setText(Double.toString(cell_2_1.getInputWeight(1)));
		
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
		lblWagaX.setFont(new Font("Tahoma", Font.PLAIN, 14));
		lblWagaX.setBounds(408, 89, 58, 23);
		frame.getContentPane().add(lblWagaX);
		
		JLabel lblWagaY = new JLabel("Waga Y");
		lblWagaY.setHorizontalAlignment(SwingConstants.CENTER);
		lblWagaY.setFont(new Font("Tahoma", Font.PLAIN, 14));
		lblWagaY.setBounds(494, 89, 58, 23);
		frame.getContentPane().add(lblWagaY);
		
		x_weight_1_1 = new JLabel("x");
		x_weight_1_1.setHorizontalAlignment(SwingConstants.CENTER);
		x_weight_1_1.setFont(new Font("Tahoma", Font.PLAIN, 14));
		x_weight_1_1.setBounds(380, 110, 90, 23);
		frame.getContentPane().add(x_weight_1_1);
		
		y_weight_1_1 = new JLabel("y");
		y_weight_1_1.setHorizontalAlignment(SwingConstants.CENTER);
		y_weight_1_1.setFont(new Font("Tahoma", Font.PLAIN, 14));
		y_weight_1_1.setBounds(480, 110, 90, 23);
		frame.getContentPane().add(y_weight_1_1);
	

		x_weight_1_2 = new JLabel("x");
		x_weight_1_2.setHorizontalAlignment(SwingConstants.CENTER);
		x_weight_1_2.setFont(new Font("Tahoma", Font.PLAIN, 14));
		x_weight_1_2.setBounds(380, 130, 90, 23);
		frame.getContentPane().add(x_weight_1_2);
		
		y_weight_1_2 = new JLabel("y");
		y_weight_1_2.setHorizontalAlignment(SwingConstants.CENTER);
		y_weight_1_2.setFont(new Font("Tahoma", Font.PLAIN, 14));
		y_weight_1_2.setBounds(480, 130, 90, 23);
		frame.getContentPane().add(y_weight_1_2);
		

		x_weight_2_1 = new JLabel("x");
		x_weight_2_1.setHorizontalAlignment(SwingConstants.CENTER);
		x_weight_2_1.setFont(new Font("Tahoma", Font.PLAIN, 14));
		x_weight_2_1.setBounds(380, 150, 90, 23);
		frame.getContentPane().add(x_weight_2_1);
		
		y_weight_2_1 = new JLabel("y");
		y_weight_2_1.setHorizontalAlignment(SwingConstants.CENTER);
		y_weight_2_1.setFont(new Font("Tahoma", Font.PLAIN, 14));
		y_weight_2_1.setBounds(480, 150, 90, 23);
		frame.getContentPane().add(y_weight_2_1);
	}
	
     private void addRandomPoint()
     {
     	// Generate two numbers
     	Random r = new Random();
     	
     	// Pass them to the neural cell
		cell_1_1.setInputData(0, (r.nextInt()%100)/100);
		cell_1_1.setInputData(1, (r.nextInt()%100)/100);
     	
		cell_1_2.setInputData(0, (r.nextInt()%100)/100);
		cell_1_2.setInputData(1, (r.nextInt()%100)/100);
     	
		// second layer
		System.out.println("1_1 output");
		System.out.println(cell_1_1.getOutput());
		System.out.println("1_2 output");
		System.out.println(cell_1_2.getOutput());
		cell_2_1.setInputData(0, cell_1_1.getOutput());
		cell_2_1.setInputData(1, cell_1_2.getOutput());
     	
		
     	// Get the output
		double _result = cell_2_1.getOutput();
     	System.out.println("2_1 result double");
     	System.out.println(_result);
     	
		
     	int result = (int)_result;
     	
     	System.out.println("2_1 result");
     	System.out.println(result);
     	// Draw appropriate point colour
     	
     	if(_result >= 0.7)
     		graphx.drawPoint((int)cell_1_1.getInputData(0), (int)cell_1_1.getInputData(1), Color.BLUE);
     	else
     		graphx.drawPoint((int)cell_1_1.getInputData(0), (int)cell_1_1.getInputData(1), Color.RED);
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