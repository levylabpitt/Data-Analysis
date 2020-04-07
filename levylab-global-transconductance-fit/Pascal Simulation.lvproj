<?xml version='1.0' encoding='UTF-8'?>
<Project Type="Project" LVVersion="16008000">
	<Item Name="My Computer" Type="My Computer">
		<Property Name="NI.SortType" Type="Int">3</Property>
		<Property Name="server.app.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.control.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="server.tcp.enabled" Type="Bool">false</Property>
		<Property Name="server.tcp.port" Type="Int">0</Property>
		<Property Name="server.tcp.serviceName" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.tcp.serviceName.default" Type="Str">My Computer/VI Server</Property>
		<Property Name="server.vi.callsEnabled" Type="Bool">true</Property>
		<Property Name="server.vi.propertiesEnabled" Type="Bool">true</Property>
		<Property Name="specify.custom.address" Type="Bool">false</Property>
		<Item Name="Relaxed Minimum.vi" Type="VI" URL="../Relaxed Minimum.vi"/>
		<Item Name="Interpolate Real.vi" Type="VI" URL="../Interpolate Real.vi"/>
		<Item Name="Iterative Minimization.vi" Type="VI" URL="../Newton/Iterative Minimization.vi"/>
		<Item Name="Error Function.vi" Type="VI" URL="../Error Function.vi"/>
		<Item Name="A-B Fit.vi" Type="VI" URL="../A-B Fit.vi"/>
		<Item Name="Create 2D Data Real.vi" Type="VI" URL="../Create 2D Data Real.vi"/>
		<Item Name="Create 2D Data.vi" Type="VI" URL="../Create 2D Data.vi"/>
		<Item Name="Create Template Sech2 Function.vi" Type="VI" URL="../Create Template Sech2 Function.vi"/>
		<Item Name="Err vs Lock Size Real.vi" Type="VI" URL="../Err vs Lock Size Real.vi"/>
		<Item Name="Err vs Lock Size.vi" Type="VI" URL="../Err vs Lock Size.vi"/>
		<Item Name="Generate B-Vg scales.vi" Type="VI" URL="../Generate B-Vg scales.vi"/>
		<Item Name="Get 1D B Array.vi" Type="VI" URL="../Get 1D B Array.vi"/>
		<Item Name="Interpolate Vsg.vi" Type="VI" URL="../Interpolate Vsg.vi"/>
		<Item Name="set up parameters Real.vi" Type="VI" URL="../set up parameters Real.vi"/>
		<Item Name="Shift Function.vi" Type="VI" URL="../Shift Function.vi"/>
		<Item Name="Trion Simulation Real.vi" Type="VI" URL="../Trion Simulation Real.vi"/>
		<Item Name="Trion Simulation.vi" Type="VI" URL="../Trion Simulation.vi"/>
		<Item Name="Extended Rosenbrock Function.vi" Type="VI" URL="../Static Function/Extended Rosenbrock Function.vi"/>
		<Item Name="My Golden Section 1D.vi" Type="VI" URL="../Newton/My Golden Section 1D.vi"/>
		<Item Name="Tests.vi" Type="VI" URL="../Tests.vi"/>
		<Item Name="Untitled 4.vi" Type="VI" URL="../Untitled 4.vi"/>
		<Item Name="Generate Arbitrary Mask.vi" Type="VI" URL="../Generate Arbitrary Mask.vi"/>
		<Item Name="Mask LP filter.vi" Type="VI" URL="../Mask LP filter.vi"/>
		<Item Name="Compute Sigma.vi" Type="VI" URL="../Compute Sigma.vi"/>
		<Item Name="Power Spectrum Normalization Check.vi" Type="VI" URL="../Power Spectrum Normalization Check.vi"/>
		<Item Name="Obtain Dense Array from Skeleton.vi" Type="VI" URL="../Obtain Dense Array from Skeleton.vi"/>
		<Item Name="Dependencies" Type="Dependencies">
			<Item Name="vi.lib" Type="Folder">
				<Item Name="NI_PtbyPt.lvlib" Type="Library" URL="/&lt;vilib&gt;/ptbypt/NI_PtbyPt.lvlib"/>
				<Item Name="Error Cluster From Error Code.vi" Type="VI" URL="/&lt;vilib&gt;/Utility/error.llb/Error Cluster From Error Code.vi"/>
				<Item Name="Image Type" Type="VI" URL="/&lt;vilib&gt;/vision/Image Controls.llb/Image Type"/>
				<Item Name="IMAQ Create" Type="VI" URL="/&lt;vilib&gt;/vision/Basics.llb/IMAQ Create"/>
				<Item Name="IMAQ ArrayToImage" Type="VI" URL="/&lt;vilib&gt;/vision/Basics.llb/IMAQ ArrayToImage"/>
				<Item Name="IMAQ ImageToArray" Type="VI" URL="/&lt;vilib&gt;/vision/Basics.llb/IMAQ ImageToArray"/>
				<Item Name="NI_AALPro.lvlib" Type="Library" URL="/&lt;vilib&gt;/Analysis/NI_AALPro.lvlib"/>
				<Item Name="IMAQ Image.ctl" Type="VI" URL="/&lt;vilib&gt;/vision/Image Controls.llb/IMAQ Image.ctl"/>
				<Item Name="NI_Vision_Development_Module.lvlib" Type="Library" URL="/&lt;vilib&gt;/vision/NI_Vision_Development_Module.lvlib"/>
				<Item Name="ROI Descriptor" Type="VI" URL="/&lt;vilib&gt;/vision/Image Controls.llb/ROI Descriptor"/>
				<Item Name="NI_AALBase.lvlib" Type="Library" URL="/&lt;vilib&gt;/Analysis/NI_AALBase.lvlib"/>
			</Item>
			<Item Name="lvanlys.dll" Type="Document" URL="/&lt;resource&gt;/lvanlys.dll"/>
			<Item Name="nivissvc.dll" Type="Document" URL="nivissvc.dll">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
			<Item Name="nivision.dll" Type="Document" URL="nivision.dll">
				<Property Name="NI.PreserveRelativePath" Type="Bool">true</Property>
			</Item>
		</Item>
		<Item Name="Build Specifications" Type="Build"/>
	</Item>
</Project>
