using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Drawing.Imaging;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Diagnostics;
using System.CodeDom.Compiler;
using System.Windows.Forms.VisualStyles;

namespace Screenshot

{
    public partial class Save : Form
    {
        Bitmap bmp;
        private string s_outfolder = null;

        public Save(Int32 x, Int32 y, Int32 w, Int32 h, Size s)
        {
            InitializeComponent();
            this.Text = "";
            btnSave.Text= "Save";
            btnHome.Text = "New";
            //C#: how to take a screenshot of a portion of screen https://stackoverflow.com/a/3306633/5260872
            Rectangle rect = new Rectangle(x, y, w, h);
            bmp = new Bitmap(rect.Width, rect.Height, PixelFormat.Format32bppArgb);
            Graphics g = Graphics.FromImage(bmp);
            g.CopyFromScreen(rect.Left, rect.Top, 0, 0, s, CopyPixelOperation.SourceCopy);
            //bmp.Save(@"C:\work\screen.jpeg", System.Drawing.Imaging.ImageFormat.Jpeg);
            pbCapture.Image = bmp;
            if (s_outfolder == null)
            {
                s_outfolder = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments) + "\\Screenshot";
            }
            
        }    
       
        public string saveImageFile(string data)
        {  
           string destinationTextPath = s_outfolder + "\\screenshot.out";
           System.IO.File.WriteAllText(destinationTextPath, data);
           return destinationTextPath;
        }
      
        private void btnSave_Click(object sender, EventArgs e)
        {
            
            SaveFileDialog sfd = new SaveFileDialog();
            sfd.CheckPathExists = true;
            string t = s_outfolder +"\\screenshot.txt";
            string text = System.IO.File.ReadAllText(t);
            sfd.FileName = text; 
            sfd.Filter = "PNG Image(*.png)|*.png|JPG Image(*.jpg)|*.jpg|BMP Image(*.bmp)|*.bmp";
            pbCapture.Image.Save(sfd.FileName);
            saveImageFile(sfd.FileName);
            pbCapture.Image.Dispose();
            this.Close();
            Application.Exit();
            /*
            if (sfd.ShowDialog() == DialogResult.OK)
            {
                pbCapture.Image.Save(sfd.FileName);
                // saveImageFile(sfd.FileName);
                pbCapture.Image.Dispose();
                this.Close();
                Application.Exit();
            } 
            */
        }
        private void btnHome_Click(object sender, EventArgs e)
        {
            SelectArea new_ = new  SelectArea();
            this.Hide();
            new_.Show();
        }
        private void btnExitProgram_Click(object sender, EventArgs e)
        {   
            this.Close();
            Application.Exit();
        }
                }
    }
