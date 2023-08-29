using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Windows.Input;
using System.Net;
using System.IO;
using System.Text.RegularExpressions;
using System.Runtime.InteropServices;

namespace windnd
{
    public partial class Form1 : Form
    {
        //#region DLL Imports
        //[DllImport("user32.dll", SetLastError = true)]
        //static extern bool ChangeWindowMessageFilter(uint message, uint dwFlag);

        //private const uint WM_DROPFILES = 0x233;
        //private const uint WM_COPYDATA = 0x004A;
        //private const uint WM_COPYGLOBALDATA = 0x0049;
        //private const uint MSGFLT_ADD = 1;

        //[DllImport("shell32.dll", CharSet = CharSet.Auto, SetLastError = true)]
        //private static extern int DragQueryFile(IntPtr hDrop, uint iFile, StringBuilder lpszFile, int cch);
        //#endregion

        const string UNSUPPORTED_OBJECT = "Unsupported drop object!";
        const string FILEDROP_ONLY = "Only file drop is allowed!";
        const string IMAGEDROP_ONLY = "Only image drop is allowed!";
        private string[] args;
        private bool b_filedrop = false;
        private bool b_imagedrop = false;
        private string s_outfolder = null;

        public Form1(string[] _args)
        {
            InitializeComponent();
            //ChangeWindowMessageFilter(WM_DROPFILES, MSGFLT_ADD);
            //ChangeWindowMessageFilter(WM_COPYDATA, MSGFLT_ADD);
            //ChangeWindowMessageFilter(WM_COPYGLOBALDATA, MSGFLT_ADD);
            this.args = _args;
            foreach (string arg in args)
            {
                if (arg == "-f")
                    b_filedrop = true;
                else if (arg == "-i")
                    b_imagedrop = true;
                else
                    s_outfolder = arg;
            }
            if (s_outfolder == null)
            {
                s_outfolder = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments) + "\\DragAndDrop";
                checkDir(s_outfolder);
            }
        }

        //protected override void WndProc(ref Message m)
        //{
        //    if (m.Msg == 0x0233) // WM_DROPFILES == 0x0233
        //    {
        //        int countOfFiles = DragQueryFile(m.WParam, 0xFFFFFFFF, null, 0);

        //        int error = Marshal.GetLastWin32Error();
        //        if (error != 0)
        //        {
        //            string paramValue = m.WParam.ToString("x");
        //        }

        //        for (int i = 0; i <= countOfFiles; i++)
        //        {
        //            StringBuilder sb = new StringBuilder(1024);
        //            DragQueryFile(m.WParam, (uint)i, sb, 1024);

        //            if (sb != null)
        //            {
        //                if (sb.ToString() != "")
        //                {
        //                    //this.listBox1.Items.Add(sb.ToString());
        //                    this.lb.Text += sb.ToString();
        //                }
        //            }
        //        }
        //    }

        //    base.WndProc(ref m);
        //}

        private string[] get_files(DragEventArgs e)
        {
            string[] files = (string[])e.Data.GetData(DataFormats.FileDrop);
            return files;
        }

        private string checkDir(string dirpath)
        {
            //string dirpath = Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments) + "\\" + UserPath;
            try
            {
                Directory.CreateDirectory(dirpath);
            }
            catch (IOException iox)
            {
                //Console.WriteLine(iox.Message + " " + iox.Data);
            }
            return dirpath;
        }

        public string saveImageFile(string ext, byte[] bytes)
        {
            string destinationImgPath = s_outfolder + "\\image" + ext;
            //checkDir(UserImagesPath);
            //var bytes = Convert.FromBase64String(base64Image);
            using (var imageFile = new FileStream(destinationImgPath, FileMode.Create))
            {
                imageFile.Write(bytes, 0, bytes.Length);
                imageFile.Flush();
            }
            return destinationImgPath;
        }

        private string get_image_file(string data)
        {
            var regMatch = Regex.Match(data, @"data:image/(?<type>.+?),(?<data>.+)").Groups;
            var ext = "." + regMatch["type"].Value.Split(';')[0];
            var base64Data = regMatch["data"].Value;
            var binData = Convert.FromBase64String(base64Data);
            //using (var stream = new MemoryStream(binData))
            //{
            //    var pictureBox = new PictureBox
            //    {
            //        Image = new Bitmap(stream),
            //    };
            //    var form = new Form { AutoSize = true, AutoSizeMode = AutoSizeMode.GrowAndShrink };
            //    form.Controls.Add(pictureBox);
            //    Application.Run(form);
            //}
            return saveImageFile(ext, binData);
        }

        public string saveTextFile(string data)
        {
            string destinationTextPath = s_outfolder + "\\windnd.out";
            //checkDir(s_outfile);
            System.IO.File.WriteAllText(destinationTextPath, data);
            return destinationTextPath;
        }

        private string get_text_file(string data)
        {
            return saveTextFile(data);
        }

        private void lb_DragEnter(object sender, DragEventArgs e)
        {
            string dfs = get_dataformat(e);
            lb.Text = dfs;
            e.Effect = DragDropEffects.Copy;
        }

        private string get_drop(DragEventArgs e)
        {
            string r = "";
            if (e.Data.GetDataPresent(DataFormats.FileDrop))
            {
                if (b_imagedrop)
                    return IMAGEDROP_ONLY;
                foreach (string file in get_files(e))
                {
                    r = file;
                    return r;
                }
            }
            if (b_filedrop)
                return FILEDROP_ONLY;
            if (e.Data.GetDataPresent(DataFormats.Text) || e.Data.GetDataPresent(DataFormats.Html))
            {
                r = e.Data.GetData(DataFormats.Text).ToString();
                if (r.StartsWith(@"data:image/"))
                    return get_image_file(r);
                if ((r.StartsWith("https://") || r.StartsWith("http://")) && 
                    (r.ToLower().EndsWith("jpg") || r.ToLower().EndsWith("jpeg") || r.ToLower().EndsWith("png")))
                {
                    string ext;
                    if (r.ToLower().EndsWith("png"))
                        ext = ".png";
                    else
                    //if (r.ToLower().EndsWith("jpg") || r.ToLower().EndsWith("jpeg"))
                        ext = ".jpg";
                    using (var wc = new System.Net.WebClient())
                    {
                        string imgpath = s_outfolder + "\\" + "image" + ext;
                        //checkDir("DragAndDrop");
                        wc.DownloadFile(new Uri(r), imgpath);
                        return imgpath;
                    }
                }
                if (b_imagedrop)
                    return IMAGEDROP_ONLY;
                //r = get_text_file(r);
                return r;
            }
            if (b_imagedrop)
                return IMAGEDROP_ONLY;
            if (e.Data.GetDataPresent(DataFormats.Text))
            {
                r = e.Data.GetData(DataFormats.Text).ToString();
                //r = get_text_file(r);
                return r;
            }
            //if (e.Data.GetDataPresent(DataFormats.OemText))
            //{
            //    r = e.Data.GetData(DataFormats.OemText).ToString();
            //    return r;
            //}
            //if (e.Data.GetDataPresent(DataFormats.Html))
            //{
            //    r = e.Data.GetData(DataFormats.Html).ToString();
            //    return r;
            //}
            //if (e.Data.GetDataPresent(DataFormats.Bitmap))
            //    r = ", " + DataFormats.Bitmap;
            //if (e.Data.GetDataPresent(DataFormats.CommaSeparatedValue))
            //    r += "," + DataFormats.CommaSeparatedValue;
            //if (e.Data.GetDataPresent(DataFormats.Dib))
            //    r += "," + DataFormats.Dib;
            //if (e.Data.GetDataPresent(DataFormats.Dif))
            //    r += "," + DataFormats.Dif;
            //if (e.Data.GetDataPresent(DataFormats.EnhancedMetafile))
            //    r += "," + DataFormats.EnhancedMetafile;
            //if (e.Data.GetDataPresent(DataFormats.Locale))
            //    r += "," + DataFormats.Locale;
            //if (e.Data.GetDataPresent(DataFormats.MetafilePict))
            //    r += "," + DataFormats.MetafilePict;
            //if (e.Data.GetDataPresent(DataFormats.Palette))
            //    r += "," + DataFormats.Palette;
            //if (e.Data.GetDataPresent(DataFormats.PenData))
            //    r += "," + DataFormats.PenData;
            //if (e.Data.GetDataPresent(DataFormats.Riff))
            //    r += "," + DataFormats.Riff;
            //if (e.Data.GetDataPresent(DataFormats.Rtf))
            //    r += "," + DataFormats.Rtf;
            //if (e.Data.GetDataPresent(DataFormats.Serializable))
            //    r += "," + DataFormats.Serializable;
            //if (e.Data.GetDataPresent(DataFormats.StringFormat))
            //    r += "," + DataFormats.StringFormat;
            //if (e.Data.GetDataPresent(DataFormats.SymbolicLink))
            //    r += "," + DataFormats.SymbolicLink;
            //if (e.Data.GetDataPresent(DataFormats.Tiff))
            //    r += "," + DataFormats.Tiff;
            //if (e.Data.GetDataPresent(DataFormats.WaveAudio))
            //    r += "," + DataFormats.WaveAudio;
            //return r;
            return UNSUPPORTED_OBJECT;
        }


        private void lb_DragDrop(object sender, DragEventArgs e)
        {
            string drop_result = get_drop(e);
            lb.Text = drop_result;
            //MessageBox.Show(drop_result);
            if (drop_result == UNSUPPORTED_OBJECT || drop_result == FILEDROP_ONLY || drop_result == IMAGEDROP_ONLY)
                return;     // do nothing
            //Console.WriteLine(drop_result);
            saveTextFile(drop_result);
            this.Close();
        }

        private void lb_DragLeave(object sender, EventArgs e)
        {
            //lbTitle.Text = "Drop any file or image to use in ARGOS RPA+ Bot";
        }

        private void set_image_url(string url)
        {
            //lbTitle.Text = url;
            using (var client = new WebClient())
            {
                //Environment.GetEnvironmentVariable("TEMP");
                string imgTempFile = Path.GetTempFileName();
                client.DownloadFile(url, imgTempFile);
                //pb.Load(imgTempFile);
                //pb.Image = Bitmap.FromFile(imgTempFile);
            }
        }

        private string get_dataformat(DragEventArgs e)
        {
            string r = "";
            if (e.Data.GetDataPresent(DataFormats.Bitmap))
            {
                if (r.Length > 0) r += ",";
                r += DataFormats.Bitmap;
            }
            if (e.Data.GetDataPresent(DataFormats.CommaSeparatedValue))
            {
                if (r.Length > 0) r += ",";
                r += DataFormats.CommaSeparatedValue;
            }
            if (e.Data.GetDataPresent(DataFormats.Dib))
            {
                if (r.Length > 0) r += ",";
                r += DataFormats.Dib;
            }
            if (e.Data.GetDataPresent(DataFormats.Dif))
            {
                if (r.Length > 0) r += ",";
                r += DataFormats.Dif;
            }
            if (e.Data.GetDataPresent(DataFormats.EnhancedMetafile))
            {
                if (r.Length > 0) r += ",";
                r += DataFormats.EnhancedMetafile;
            }
            if (e.Data.GetDataPresent(DataFormats.FileDrop))
            {
                if (r.Length > 0) r += ",";
                r += DataFormats.FileDrop;
            }
            if (e.Data.GetDataPresent(DataFormats.Html))
            {
                if (r.Length > 0) r += ",";
                r += DataFormats.Html;
            }
            if (e.Data.GetDataPresent(DataFormats.Locale))
            {
                if (r.Length > 0) r += ",";
                r += DataFormats.Locale;
            }
            if (e.Data.GetDataPresent(DataFormats.MetafilePict))
            {
                if (r.Length > 0) r += ",";
                r += DataFormats.MetafilePict;
            }
            if (e.Data.GetDataPresent(DataFormats.OemText))
            {
                if (r.Length > 0) r += ",";
                r += DataFormats.OemText;
            }
            if (e.Data.GetDataPresent(DataFormats.Palette))
            {
                if (r.Length > 0) r += ",";
                r += DataFormats.Palette;
            }
            if (e.Data.GetDataPresent(DataFormats.PenData))
            {
                if (r.Length > 0) r += ",";
                r += DataFormats.PenData;
            }
            if (e.Data.GetDataPresent(DataFormats.Riff))
            {
                if (r.Length > 0) r += ",";
                r += DataFormats.Riff;
            }
            if (e.Data.GetDataPresent(DataFormats.Rtf))
            {
                if (r.Length > 0) r += ",";
                r += DataFormats.Rtf;
            }
            if (e.Data.GetDataPresent(DataFormats.Serializable))
            {
                if (r.Length > 0) r += ",";
                r += DataFormats.Serializable;
            }
            if (e.Data.GetDataPresent(DataFormats.StringFormat))
            {
                if (r.Length > 0) r += ",";
                r += DataFormats.StringFormat;
            }
            if (e.Data.GetDataPresent(DataFormats.SymbolicLink))
            {
                if (r.Length > 0) r += ",";
                r += DataFormats.SymbolicLink;
            }
            if (e.Data.GetDataPresent(DataFormats.Text))
            {
                if (r.Length > 0) r += ",";
                r += DataFormats.Text;
            }
            if (e.Data.GetDataPresent(DataFormats.Tiff))
            {
                if (r.Length > 0) r += ",";
                r += DataFormats.Tiff;
            }
            if (e.Data.GetDataPresent(DataFormats.UnicodeText))
            {
                if (r.Length > 0) r += ",";
                r += DataFormats.UnicodeText;
            }
            if (e.Data.GetDataPresent(DataFormats.WaveAudio))
            {
                if (r.Length > 0) r += ",";
                r += DataFormats.WaveAudio;
            }
            return r;
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            //ChangeWindowMessageFilter(WM_DROPFILES, MSGFLT_ADD);
            //ChangeWindowMessageFilter(WM_COPYDATA, MSGFLT_ADD);
            //ChangeWindowMessageFilter(WM_COPYGLOBALDATA, MSGFLT_ADD);
        }

        private void lb_DragOver(object sender, DragEventArgs e)
        {
            //e.Effect = DragDropEffects.Move;
            //this.Cursor = Cursors.Hand;
            //Cursor.Current = Cursors.Hand;
        }

        private void lb_GiveFeedback(object sender, GiveFeedbackEventArgs e)
        {
            //e.UseDefaultCursors = false;
            if (e.Effect == DragDropEffects.Copy)
            {
                e.UseDefaultCursors = false;
                this.Cursor = Cursors.Hand;
            }
            else
                e.UseDefaultCursors = true;
            //e.Handled = true;
        }
    }
}
