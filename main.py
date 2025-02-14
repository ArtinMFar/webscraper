#!/usr/bin/env python3
import re
import requests
from flask import Flask, request, render_template_string
from bs4 import BeautifulSoup

app = Flask(__name__)

# A multiline string containing all the valid names (one per line)
ITEMS_RAW = """Accessory
AccessoryDescription
Accoutrement
Actor
AdGui
AdPortal
AdService
AdvancedDragger
AirController
AlignOrientation
AlignPosition
AnalyticsService
AngularVelocity
Animation
AnimationClip
AnimationClipProvider
AnimationConstraint
AnimationController
AnimationFromVideoCreatorService
AnimationRigData
AnimationTrack
Animator
Annotation
ArcHandles
AssetDeliveryProxy
AssetPatchSettings
AssetService
Atmosphere
AtmosphereSensor
Attachment
AudioAnalyzer
AudioChannelMixer
AudioChannelSplitter
AudioChorus
AudioCompressor
AudioDeviceInput
AudioDeviceOutput
AudioDistortion
AudioEcho
AudioEmitter
AudioEqualizer
AudioFader
AudioFilter
AudioFlanger
AudioLimiter
AudioListener
AudioPages
AudioPitchShifter
AudioPlayer
AudioReverb
AudioSearchParams
AvatarCreationService
AvatarEditorService
Backpack
BackpackItem
BadgeService
BallSocketConstraint
BanHistoryPages
BasePart
BasePlayerGui
BaseRemoteEvent
BaseScript
BaseWrap
Beam
BevelMesh
BillboardGui
BinaryStringValue
BindableEvent
BindableFunction
BlockMesh
BloomEffect
BlurEffect
BodyAngularVelocity
BodyColors
BodyForce
BodyGyro
BodyMover
BodyPartDescription
BodyPosition
BodyThrust
BodyVelocity
Bone
BoolValue
BoxHandleAdornment
BrickColorValue
BrowserService
BubbleChatConfiguration
BubbleChatMessageProperties
BuoyancySensor
CacheableContentProvider
Camera
CanvasGroup
CaptureService
CatalogPages
CFrameValue
ChangeHistoryService
ChannelTabsConfiguration
CharacterAppearance
CharacterMesh
Chat
ChatInputBarConfiguration
ChatWindowConfiguration
ChatWindowMessageProperties
ChorusSoundEffect
ClickDetector
ClientReplicator
ClimbController
Clothing
Clouds
ClusterPacketCache
CollectionService
Color3Value
ColorCorrectionEffect
ColorGradingEffect
CommandService
CommerceService
CompressorSoundEffect
ConeHandleAdornment
Configuration
ConfigureServerService
Constraint
ContentProvider
ContextActionService
Controller
ControllerBase
ControllerManager
ControllerPartSensor
ControllerSensor
ControllerService
CookiesService
CoreGui
CoreScriptDebuggingManagerHelper
CornerWedgePart
CreatorStoreService
CurveAnimation
CustomEvent
CustomEventReceiver
CylinderHandleAdornment
CylinderMesh
CylindricalConstraint
DataModel
DataModelMesh
DataModelSession
DataStore
DataStoreGetOptions
DataStoreIncrementOptions
DataStoreInfo
DataStoreKey
DataStoreKeyInfo
DataStoreKeyPages
DataStoreListingPages
DataStoreObjectVersionInfo
DataStoreOptions
DataStorePages
DataStoreService
DataStoreSetOptions
DataStoreVersionPages
Debris
DebugSettings
Decal
DepthOfFieldEffect
Dialog
DialogChoice
DistortionSoundEffect
DockWidgetPluginGui
DoubleConstrainedValue
DraftsService
DragDetector
Dragger
DraggerService
DynamicRotate
EchoSoundEffect
EditableImage
EditableMesh
EmotesPages
EqualizerSoundEffect
EulerRotationCurve
ExperienceInviteOptions
ExperienceNotificationService
Explosion
FaceControls
FaceInstance
Feature
FeatureRestrictionManager
File
FileMesh
Fire
Flag
FlagStand
FlagStandService
FlangeSoundEffect
FloatCurve
FloorWire
FluidForceSensor
Folder
ForceField
FormFactorPart
Frame
FriendPages
FriendService
FunctionalTest
GamepadService
GamePassService
GameSettings
GenericChallengeService
GenericSettings
Geometry
GeometryService
GetTextBoundsParams
GlobalDataStore
GlobalSettings
Glue
GoogleAnalyticsConfiguration
GroundController
GroupService
GuiBase
GuiBase2d
GuiBase3d
GuiButton
GuidRegistryService
GuiLabel
GuiMain
GuiObject
GuiService
HandleAdornment
Handles
HandlesBase
HapticService
Hat
HeightmapImporterService
HiddenSurfaceRemovalAsset
Highlight
HingeConstraint
Hint
Hole
Hopper
HopperBin
HSRDataContentProvider
HttpRbxApiService
HttpService
Humanoid
HumanoidController
HumanoidDescription
IKControl
ILegacyStudioBridge
ImageButton
ImageHandleAdornment
ImageLabel
IncrementalPatchBuilder
InputObject
InsertService
Instance
InstanceAdornment
IntConstrainedValue
IntersectOperation
IntValue
InventoryPages
JointInstance
JointsService
KeyboardService
Keyframe
KeyframeMarker
KeyframeSequence
KeyframeSequenceProvider
LanguageService
LayerCollector
Light
Lighting
LinearVelocity
LineForce
LineHandleAdornment
LocalizationService
LocalizationTable
LocalScript
LoginService
LogService
LuaSettings
LuaSourceContainer
LuaWebService
ManualGlue
ManualSurfaceJointInstance
ManualWeld
MarkerCurve
MarketplaceService
MaterialService
MaterialVariant
MemoryStoreHashMap
MemoryStoreHashMapPages
MemoryStoreQueue
MemoryStoreService
MemoryStoreSortedMap
MemStorageConnection
MemStorageService
MeshContentProvider
MeshPart
Message
MessagingService
Model
ModuleScript
Motor
Motor6D
MotorFeature
Mouse
MouseService
MultipleDocumentInterfaceInstance
NegateOperation
NetworkClient
NetworkMarker
NetworkPeer
NetworkReplicator
NetworkServer
NetworkSettings
NoCollisionConstraint
NotificationService
NumberPose
NumberValue
Object
ObjectValue
OpenCloudApiV1
OpenCloudService
OrderedDataStore
OutfitPages
PackageLink
PackageService
Pages
Pants
Part
PartAdornment
ParticleEmitter
PartOperation
PartOperationAsset
PatchBundlerFileWatch
PatchMapping
Path
Path2D
PathfindingLink
PathfindingModifier
PathfindingService
PermissionsService
PhysicsService
PhysicsSettings
PitchShiftSoundEffect
PlacesService
Plane
PlaneConstraint
Platform
Player
PlayerGui
PlayerMouse
Players
PlayerScripts
PlayerViewService
Plugin
PluginAction
PluginCapabilities
PluginDebugService
PluginDragEvent
PluginGui
PluginGuiService
PluginManagementService
PluginManager
PluginManagerInterface
PluginMenu
PluginMouse
PluginToolbar
PluginToolbarButton
PointLight
PointsService
PolicyService
Pose
PoseBase
PostEffect
PrismaticConstraint
ProcessInstancePhysicsService
ProximityPrompt
ProximityPromptService
PublishService
PVAdornment
PVInstance
QWidgetPluginGui
RayValue
ReflectionMetadata
ReflectionMetadataCallbacks
ReflectionMetadataClass
ReflectionMetadataClasses
ReflectionMetadataEnum
ReflectionMetadataEnumItem
ReflectionMetadataEnums
ReflectionMetadataEvents
ReflectionMetadataFunctions
ReflectionMetadataItem
ReflectionMetadataMember
ReflectionMetadataProperties
ReflectionMetadataYieldFunctions
RemoteDebuggerServer
RemoteEvent
RemoteFunction
RenderingTest
RenderSettings
ReplicatedFirst
ReplicatedStorage
ReverbSoundEffect
RigidConstraint
RocketPropulsion
RodConstraint
RopeConstraint
Rotate
RotateP
RotateV
RotationCurve
RunningAverageItemDouble
RunningAverageItemInt
RunningAverageTimeIntervalItem
RunService
ScreenGui
ScreenshotHud
Script
ScriptBuilder
ScriptContext
ScriptDocument
ScriptEditorService
ScriptProfilerService
ScriptService
ScrollingFrame
Seat
Selection
SelectionBox
SelectionHighlightManager
SelectionLasso
SelectionPartLasso
SelectionPointLasso
SelectionSphere
SensorBase
ServerReplicator
ServerScriptService
ServerStorage
ServiceProvider
ServiceVisibilityService
SharedTableRegistry
Shirt
ShirtGraphic
ShorelineUpgraderService
SkateboardController
SkateboardPlatform
Skin
Sky
SlidingBallConstraint
Smoke
SmoothVoxelsUpgraderService
Snap
SocialService
SolidModelContentProvider
Sound
SoundEffect
SoundGroup
SoundService
Sparkles
SpawnerService
SpawnLocation
SpecialMesh
SphereHandleAdornment
SpotLight
SpringConstraint
StandalonePluginScripts
StandardPages
StarterCharacterScripts
StarterGear
StarterGui
StarterPack
StarterPlayer
StarterPlayerScripts
StartupMessageService
Stats
StatsItem
Status
StopWatchReporter
StringValue
Studio
StudioService
StudioTheme
StyleBase
StyleDerive
StyleLink
StyleRule
StyleSheet
SunRaysEffect
SurfaceAppearance
SurfaceGui
SurfaceGuiBase
SurfaceLight
SurfaceSelection
SwimController
SyncScriptBuilder
TaskScheduler
Team
TeamCreateData
TeamCreateService
Teams
TeleportAsyncResult
TeleportOptions
TeleportService
Terrain
TerrainDetail
TerrainRegion
TestService
TextBox
TextBoxService
TextButton
TextChannel
TextChatCommand
TextChatConfigurations
TextChatMessage
TextChatMessageProperties
TextChatService
TextFilterResult
TextFilterTranslatedResult
TextLabel
TextService
TextSource
Texture
TimerService
Tool
Torque
TorsionSpringConstraint
TotalCountTimeIntervalItem
TouchInputService
TouchTransmitter
Trail
Translator
TremoloSoundEffect
TriangleMeshPart
TrussPart
Tween
TweenBase
TweenService
UGCValidationService
UIAspectRatioConstraint
UIBase
UIComponent
UIConstraint
UICorner
UIDragDetector
UIFlexItem
UIGradient
UIGridLayout
UIGridStyleLayout
UILayout
UIListLayout
UIPadding
UIPageLayout
UIScale
UISizeConstraint
UIStroke
UITableLayout
UITextSizeConstraint
UnionOperation
UniversalConstraint
UnreliableRemoteEvent
UserGameSettings
UserInputService
UserService
UserSettings
ValueBase
Vector3Curve
Vector3Value
VectorForce
VehicleController
VehicleSeat
VelocityMotor
VideoCaptureService
VideoFrame
VideoPlayer
VideoService
ViewportFrame
VirtualInputManager
VirtualUser
VisibilityCheckDispatcher
Visit
VisualizationMode
VisualizationModeCategory
VisualizationModeService
VoiceChatService
VRService
VRStatusService
WedgePart
Weld
WeldConstraint
Wire
WireframeHandleAdornment
Workspace
WorkspaceAnnotation
WorldModel
WorldRoot
WrapDeformer
WrapLayer
WrapTarget"""

# Convert the raw string into a Python list (trimming whitespace)
VALID_TERMS = [line.strip() for line in ITEMS_RAW.splitlines() if line.strip()]

# Base URLs
START_URL = "https://create.roblox.com/docs/reference/engine/classes/"
ALT_URLS = [
    "https://create.roblox.com/docs/reference/engine/datatypes/",
    "https://create.roblox.com/docs/reference/engine/enums/",
    "https://create.roblox.com/docs/reference/engine/libraries/"
]

def fetch_page(url):
    """Attempts to GET the page and returns the text if successful; otherwise, returns None."""
    try:
        r = requests.get(url)
        if r.status_code == 200:
            return r.text
    except Exception as e:
        print(f"Error fetching {url}: {e}")
    return None

def scrape_content(html):
    """Use BeautifulSoup to extract a simple text version of the page."""
    soup = BeautifulSoup(html, 'html.parser')
    # You can adjust the extraction logic here if needed.
    return soup.get_text()

@app.route('/')
def index():
    # Expect a URL like: https://yourserver.com/?search=(Accessory)%20(WrapLayer)%20(WrapDeformer)%20(WorldRoot)
    search_query = request.args.get('search', '')
    # Use regex to extract all terms wrapped in parentheses
    terms = re.findall(r'\(([^)]+)\)', search_query)
    
    if not terms:
        return render_template_string("<html><body><h2>Please provide a search query in the form ?search=(term1) (term2) ...</h2></body></html>")
    
    output_sections = []
    not_found_terms = []

    for term in terms:
        term = term.strip()
        page_text = None
        used_url = None

        # If the term is in our VALID_TERMS list, try the classes URL first.
        if term in VALID_TERMS:
            candidate_url = START_URL + term
            html = fetch_page(candidate_url)
            if html:
                used_url = candidate_url
                page_text = scrape_content(html)

        # If not found using classes OR the term is not in our list,
        # try the alternate URLs.
        if not page_text:
            for base in ALT_URLS:
                candidate_url = base + term
                html = fetch_page(candidate_url)
                if html:
                    used_url = candidate_url
                    page_text = scrape_content(html)
                    break  # Stop on the first successful fetch

        if page_text:
            section = f"<h3>Start of {term} (from {used_url})</h3>\n<pre>{page_text}</pre>"
            output_sections.append(section)
        else:
            not_found_terms.append(term)
    
    final_message = ""
    if not_found_terms:
        final_message = "<p style='color:red;'>The following term(s) were not found: " + ", ".join(not_found_terms) + ".<br>" \
                        "The thing you are trying to search was not found, but don't worry as you can try other queries.</p>"
    
    # Render the combined output as a simple HTML page.
    html_output = """
    <html>
      <head>
        <meta charset="utf-8">
        <title>Roblox Docs Search Results</title>
      </head>
      <body>
        {% for section in sections %}
          {{ section|safe }}
          <hr>
        {% endfor %}
        {{ final_message|safe }}
      </body>
    </html>
    """
    return render_template_string(html_output, sections=output_sections, final_message=final_message)

if __name__ == '__main__':
    # Run the Flask development server.
    app.run(debug=True)
